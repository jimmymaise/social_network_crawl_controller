from datetime import datetime

import more_itertools

from core.utils.common import Common
from core.utils.exceptions import ErrorStoreFormat
from core.workflows.transform.base_item_transform_handler import BaseItemTransformHandler
from core.workflows.transform.stored_object.stored_object_builder import StoredObjectBuilder
from social_networks.tiktok.utils.constant import Constant
from social_networks.tiktok.workflow.transform.collected_object_schemas.collected_post_schema import \
    PostObjectSchema
from social_networks.tiktok.workflow.transform.collected_object_schemas.collected_user_schema import UserObjectSchema


class PostsCollectionTransformHandler(BaseItemTransformHandler):
    def __init__(self, service_name):
        super().__init__(service_name)

    def process_item(self, loaded_item, collected_data):
        collected_data_chunks_iter = more_itertools.ichunked(collected_data, Constant.DEFAULT_TRANSFORM_ITEM_BATCH)
        latest_posts = []
        statistics = {
            'num_post': 0,
            'num_view': 0,
            'num_like': 0,
            'num_share': 0,
            'num_comment': 0,
            'analyzed_post_from': None,
            'analyzed_post_to': None,
        }
        for collected_data_chunk in collected_data_chunks_iter:
            posts_objects = []
            user_objects = []

            # Save posts and user
            for item in collected_data_chunk:
                # upload media first
                media = self._parse_item_media_to_stored_object_lists(item=item)
                yield self._make_transformed_item(
                    collection_name=Constant.COLLECTION_NAME_MEDIA,
                    updated_object_list=[media])
                self._parse_item_to_stored_object_lists(item=item,
                                                        latest_posts=latest_posts,
                                                        user_objects=user_objects,
                                                        posts_objects=posts_objects, statistics=statistics)
            yield self._make_transformed_item(
                collection_name=Constant.COLLECTION_NAME_POST,
                updated_object_list=posts_objects)

            yield self._make_transformed_item(
                collection_name=Constant.COLLECTION_NAME_USER,
                updated_object_list=user_objects)

        yield self._make_transformed_item(
            collection_name=Constant.COLLECTION_NAME_USER,
            updated_object_list=[self._build_user_interaction_updated_object(loaded_item=loaded_item, statistics=statistics, latest_posts=latest_posts)])

        yield self._make_transformed_item(
            collection_name=Constant.COLLECTION_NAME_KOL,
            updated_object_list=[self._build_kol_updated_object(loaded_item)])

    def _parse_item_to_stored_object_lists(self, item, latest_posts, posts_objects, user_objects, statistics):
        post_data, collected_post_schema_error = self._validate_schema(data=item['post'], schema=PostObjectSchema)

        if collected_post_schema_error:
            raise ErrorStoreFormat(f'Schema error {str(collected_post_schema_error)}')

        # save posts
        posts_objects.append(self._build_post_updated_object(item))

        # Build statistics
        self._parse_item_to_statistics(post_data, statistics, latest_posts)

        if item.get('user'):
            _, collected_user_schema_error = self._validate_schema(data=item['user'],
                                                                   schema=UserObjectSchema)
            if not collected_user_schema_error:
                user_objects.append(self._build_user_updated_object(item))

            else:
                self.logger.warning(f'User transform schema error {collected_user_schema_error}')

    @staticmethod
    def _parse_item_to_statistics(post, statistics, latest_posts):
        # Build latest posts: Get 30 latest ids
        if len(latest_posts) < 30:
            latest_posts.append(post['_id'])

        # Build statistics
        statistics['num_post'] += 1
        statistics['num_view'] += post['num_view']
        statistics['num_like'] += post['num_like']
        statistics['num_share'] += post['num_share']
        statistics['num_comment'] += post['num_comment']
        if statistics['analyzed_post_from'] is None or statistics['analyzed_post_from'] > post['taken_at_timestamp']:
            statistics['analyzed_post_from'] = post['taken_at_timestamp']
        if statistics['analyzed_post_to'] is None or statistics['analyzed_post_to'] < post['taken_at_timestamp']:
            statistics['analyzed_post_to'] = post['taken_at_timestamp']

    def _parse_item_media_to_stored_object_lists(self, item):
        if item.get('post', {}).get('display_url'):
            return self._build_media_updated_object(item_having_media=item['post'], mapping={'display_url': 'link'}, media_type='display_url')

    def _build_post_updated_object(self, collected_item):
        posts_stored_object_builder = StoredObjectBuilder()
        posts_stored_object_builder.set_get_all_fields_from_collected_object('collected_post', excluded_fields=None)

        post_stored_object = posts_stored_object_builder.build(collected_post=collected_item['post'])
        post_stored_object['updated_at'] = datetime.now().timestamp()
        post_stored_object['_id'] = self._get_image_id_from_social_url(url=collected_item['post']['display_url'])
        post_stored_object = self._make_updated_object(
            filter_={'_id': post_stored_object['_id']},
            stored_object=post_stored_object,
            upsert=True
        )

        return post_stored_object

    def _build_user_updated_object(self, collected_item):
        user_stored_object_builder = StoredObjectBuilder()
        user_stored_object_builder.set_get_all_fields_from_collected_object('collected_user',
                                                                            excluded_fields='avatar')

        user_stored_object = user_stored_object_builder.build(collected_user=collected_item['user'])
        user_stored_object['avatar'] = Common.md5_hash(collected_item['user']['avatar'])

        user_updated_object = self._make_updated_object(
            filter_={'_id': user_stored_object['_id']},
            stored_object=user_stored_object,
            upsert=True
        )
        return user_updated_object

    def _build_kol_updated_object(self, collected_data):
        kol_stored_object_builder = StoredObjectBuilder()
        kol_stored_object_builder.add_mapping('collected_user', {'_id': 'user_id', 'username': 'username'}, )
        kol_stored_object_builder.set_get_all_fields_from_collected_object('report_statuses', None)

        kol_stored_object = kol_stored_object_builder.build(collected_user=collected_data,
                                                            report_statuses=self._build_kol_statuses_object()
                                                            )
        kol_updated_object = self._make_updated_object(
            filter_={'username': kol_stored_object['username']},
            stored_object=kol_stored_object,
            upsert=False
        )

        return kol_updated_object

    def _build_user_interaction_updated_object(self, loaded_item, statistics, latest_posts):
        last_time_analyze = int(datetime.now().timestamp())
        interaction = {
            'average_view': int(statistics['num_view'] / statistics['num_post']),
            'average_like': int(statistics['num_like'] / statistics['num_post']),
            'average_comment': int(statistics['num_comment'] / statistics['num_post']),
            'average_share': int(statistics['num_share'] / statistics['num_post']),
            'average_engagement': int(statistics['num_like'] + statistics['num_comment'] + statistics['num_share']
                                      / statistics['num_post']),
        }

        user_updated_object = self._make_updated_object(
            filter_={'username': loaded_item['username']},
            stored_object={
                'latest_posts': latest_posts,
                'interaction': {
                    **interaction,
                    'video': interaction,
                    'analyzed_post_to': statistics['analyzed_post_to'],
                    'analyzed_post_from': statistics['analyzed_post_from'],
                    'last_time_analyze': last_time_analyze,
                }
            },
            upsert=False
        )

        return user_updated_object

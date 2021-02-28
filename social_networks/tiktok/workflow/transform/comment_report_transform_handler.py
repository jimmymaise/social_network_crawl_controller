from datetime import datetime

import more_itertools

from core.utils.common import Common
from core.utils.exceptions import ErrorStoreFormat
from core.workflows.transform.base_item_transform_handler import BaseItemTransformHandler
from core.workflows.transform.stored_object.stored_object_builder import StoredObjectBuilder
from social_networks.tiktok.utils.constant import Constant
from social_networks.tiktok.workflow.transform.collected_object_schemas.collected_comment_schema import \
    CommentObjectSchema
from social_networks.tiktok.workflow.transform.collected_object_schemas.collected_user_schema import UserObjectSchema


class CommentReportTransformHandler(BaseItemTransformHandler):
    def __init__(self, service_name):
        super().__init__(service_name)

    def process_item(self, loaded_item, collected_data):
        collected_data_chunks_iter = more_itertools.ichunked(collected_data, Constant.DEFAULT_TRANSFORM_ITEM_BATCH)
        for collected_data_chunk in collected_data_chunks_iter:
            comment_objects = []
            post_comment_objects = []
            user_objects = []
            media_objects = []

            for item in collected_data_chunk:
                self._parse_item_to_stored_object_lists(item=item,
                                                        loaded_item=loaded_item,
                                                        comment_objects=comment_objects,
                                                        user_objects=user_objects,
                                                        media_objects=media_objects,
                                                        post_comment_objects=post_comment_objects)

            yield self._make_transformed_item(
                collection_name=Constant.COLLECTION_NAME_COMMENT,
                updated_object_list=comment_objects)

            yield self._make_transformed_item(
                collection_name=Constant.COLLECTION_NAME_POST_COMMENT,
                updated_object_list=post_comment_objects)

            yield self._make_transformed_item(
                collection_name=Constant.COLLECTION_NAME_USER,
                updated_object_list=user_objects)

            yield self._make_transformed_item(
                collection_name=Constant.COLLECTION_NAME_MEDIA,
                updated_object_list=media_objects)

        yield self._make_transformed_item(
            collection_name=Constant.COLLECTION_NAME_REPORT,
            updated_object_list=[self._build_report_updated_object(loaded_item)])

    def _parse_item_to_stored_object_lists(self, item, loaded_item, comment_objects, post_comment_objects,
                                           user_objects,
                                           media_objects):

        _, collected_comment_schema_error = self._validate_schema(data=item['comment'],
                                                                  schema=CommentObjectSchema)

        if collected_comment_schema_error:
            raise ErrorStoreFormat(f'Schema error {str(collected_comment_schema_error)}')

        post_id = loaded_item['post_id']
        comment_objects.append(self._build_comment_updated_object(item, post_id))
        post_comment_objects.append(self._build_post_comment_updated_object(item, post_id))

        if item.get('user'):
            _, collected_user_schema_error = self._validate_schema(data=item['user'],
                                                                   schema=UserObjectSchema)
            if not collected_user_schema_error:
                user_objects.append(self._build_user_updated_object(item))
                media_objects.append(self._build_media_updated_object(item['user'], mapping={'avatar': 'link'}))
            else:
                self.logger.warning(f'User transform schema error {collected_user_schema_error}')

    def _build_comment_updated_object(self, collected_item, post_id):
        comment_stored_object_builder = StoredObjectBuilder()
        comment_stored_object_builder.set_get_all_fields_from_collected_object('collected_comment',
                                                                               excluded_fields=None)

        comment_stored_object = comment_stored_object_builder.build(collected_comment=collected_item['comment'])
        comment_stored_object['post_id'] = post_id
        comment_stored_object['updated_at'] = datetime.now().timestamp()
        comment_updated_object = self._make_updated_object(
            filter_={'_id': comment_stored_object['_id']},
            stored_object=comment_stored_object,
            upsert=True
        )

        return comment_updated_object

    def _build_post_comment_updated_object(self, collected_item, post_id):
        post_comment_stored_object_builder = StoredObjectBuilder()
        post_comment_stored_object_builder.add_mapping('collected_comment',
                                                       {'_id': 'comment_id'})

        post_comment_stored_object_builder.add_mapping('collected_user',
                                                       {'_id': 'user_id'})

        post_comment_stored_object = post_comment_stored_object_builder.build(
            collected_comment=collected_item['comment'],
            collected_user=collected_item.get('user'),
        )
        post_comment_stored_object['post_id'] = post_id
        post_comment_stored_object['_id'] = Common.md5_hash(f'{post_comment_stored_object["post_id"]}'
                                                            f'{post_comment_stored_object["comment_id"]}'
                                                            f'{post_comment_stored_object.get("user_id", "")}')

        post_comment_stored_object = self._make_updated_object(
            filter_={'_id': post_comment_stored_object['_id']},
            stored_object=post_comment_stored_object,
            upsert=True
        )
        return post_comment_stored_object

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

    def _build_media_updated_object(self, item_having_media, mapping):

        media_stored_object_builder = StoredObjectBuilder()
        media_stored_object_builder.add_mapping('item', mapping)
        media_stored_object = media_stored_object_builder.build(item=item_having_media)
        media_stored_object['_id'] = Common.md5_hash(media_stored_object['link'])
        return self._make_updated_object(
            filter_={'_id': media_stored_object['_id']},
            stored_object=media_stored_object,
            upsert=True
        )

    def _build_report_updated_object(self, loaded_item):

        report_builder = StoredObjectBuilder()
        report_builder.set_get_all_fields_from_collected_object('report_statuses', None)
        report_stored_object = report_builder.build(report_statuses=self._build_report_statuses_object())
        report_stored_object['_id'] = loaded_item['_id']
        report_updated_object = self._make_updated_object(
            filter_={'_id': loaded_item['_id']},
            stored_object=report_stored_object,
            upsert=False
        )
        return report_updated_object

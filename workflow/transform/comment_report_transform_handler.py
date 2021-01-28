from datetime import datetime

import more_itertools

from core.utils.common import Common
from core.utils.constant import Constant
from workflow.transform.base_item_transform_handler import BaseItemTransformHandler
from workflow.transform.stored_object.stored_object_builder import StoredObjectBuilder


class CommentReportTransformHandler(BaseItemTransformHandler):
    def __init__(self, service_name):
        super().__init__(service_name)

    def process_item(self, loaded_item, collected_data):
        collected_data_chunks_iter = more_itertools.ichunked(collected_data, 50)
        for collected_data_chunk in collected_data_chunks_iter:
            comment_objects = []
            post_comment_objects = []
            user_objects = []
            media_objects = []
            page_objects = []

            for item in collected_data_chunk:
                comment_objects.append(self._build_comment_updated_object(item))
                post_comment_objects.append(self._build_post_comment_updated_object(item))
                user_objects.append(self._build_user_updated_object(item))
                page_objects.append(self._build_page_updated_object(item))

                if item.get('user'):
                    media_objects.append(self._build_media_updated_object(item['user'], mapping={'avatar': 'link'}))

            yield self._make_transformed_item(
                collection_name=Constant.COLLECTION_NAME_COMMENT,
                updated_object_list=[self._build_comment_updated_object(comment_object) for comment_object in
                                     comment_objects])

            yield self._make_transformed_item(
                collection_name=Constant.COLLECTION_NAME_POST_COMMENT,
                updated_object_list=[self._build_comment_updated_object(post_comment_object) for post_comment_object in
                                     post_comment_objects])

            yield self._make_transformed_item(
                collection_name=Constant.COLLECTION_NAME_USER,
                updated_object_list=[self._build_comment_updated_object(user_object) for user_object in user_objects])

            yield self._make_transformed_item(
                collection_name=Constant.COLLECTION_NAME_PAGE,
                updated_object_list=[self._build_comment_updated_object(page_object) for page_object in page_objects])

            yield self._make_transformed_item(
                collection_name=Constant.COLLECTION_NAME_MEDIA,
                updated_object_list=[self._build_comment_updated_object(media_object) for media_object in
                                     media_objects])

        report_object = self._build_report_updated_object(loaded_item)
        yield self._make_transformed_item(
            collection_name=Constant.COLLECTION_NAME_REPORT,
            updated_object_list=[self._build_comment_updated_object(report_object)])

    def _build_comment_updated_object(self, collected_item):
        comment_stored_object_builder = StoredObjectBuilder()
        comment_stored_object_builder.set_get_all_fields_from_collected_object('collected_comment',
                                                                               excluded_fields=None)

        comment_stored_object = comment_stored_object_builder.build(collected_comment=collected_item['comment'])

        comment_stored_object['updated_at'] = datetime.now().timestamp()
        comment_updated_object = self._make_updated_object(
            filter_={'_id': comment_stored_object['_id']},
            stored_object=comment_stored_object,
            upsert=True
        )

        return comment_updated_object

    def _build_post_comment_updated_object(self, collected_item):
        post_comment_stored_object_builder = StoredObjectBuilder()
        post_comment_stored_object_builder.add_mapping('collected_comment',
                                                       {'_id': 'comment_id',
                                                        'post_id': 'post_id'})

        post_comment_stored_object_builder.add_mapping('collected_user',
                                                       {'_id': 'user_id'})
        post_comment_stored_object_builder.add_mapping('collected_page',
                                                       {'app_id': 'user_id'})

        post_comment_stored_object = post_comment_stored_object_builder.build(
            collected_comment=collected_item['comment'],
            page=collected_item.get('page'),
            user=collected_item.get('user'),
        )
        post_comment_stored_object['_id'] = Common.md5_hash(f'{post_comment_stored_object["post_id"]}'
                                                            f'{post_comment_stored_object["comment_id"]}'
                                                            f'{post_comment_stored_object["user_id"]}')

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

        user_updated_object = self._make_updated_object(
            filter_={'_id': user_stored_object['_id']},
            stored_object=user_stored_object,
            upsert=False
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

    def _build_page_updated_object(self, collected_item):
        page_stored_object_builder = StoredObjectBuilder()
        page_stored_object_builder.set_get_all_fields_from_collected_object('collected_page',
                                                                            excluded_fields=None)

        page_stored_object = page_stored_object_builder.build(collected_page=collected_item['page'])

        page_updated_object = self._make_updated_object(
            filter_={'app_id': page_stored_object['app_id']},
            stored_object=page_stored_object,
            upsert=False
        )
        return page_updated_object

    def _build_report_updated_object(self, loaded_item):

        report_builder = StoredObjectBuilder()
        report_builder.set_get_all_fields_from_collected_object('report_statuses', None)

        report_stored_object = report_builder.build(
            report_statuses=self._build_report_statuses_object(),
        )
        report_stored_object['_id'] = loaded_item['_id']
        report_updated_object = self._make_updated_object(
            filter_={'_id': loaded_item['_id']},
            stored_object=report_stored_object,
            upsert=False
        )
        return report_updated_object

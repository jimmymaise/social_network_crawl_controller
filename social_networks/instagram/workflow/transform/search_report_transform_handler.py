from core.utils.common import Common
from core.utils.exceptions import ErrorStoreFormat
from core.workflows.transform.base_item_transform_handler import BaseItemTransformHandler
from core.workflows.transform.stored_object.stored_object_builder import StoredObjectBuilder
from social_networks.instagram.utils.constant import Constant
from social_networks.instagram.workflow.transform.collected_object_schemas.collected_post_schema import PostObjectSchema
from social_networks.instagram.workflow.transform.collected_object_schemas.collected_user_schema import UserObjectSchema


class SearchReportTransformHandler(BaseItemTransformHandler):
    def __init__(self, service_name):
        super().__init__(service_name)

    def process_item(self, loaded_item, collected_data):
        transformed_data = []
        _, collected_post_schema_error = self._validate_schema(data=collected_data['post'], schema=PostObjectSchema)

        if collected_post_schema_error:
            raise ErrorStoreFormat(f'Schema error {str(collected_post_schema_error)}')

        transformed_data.append(self._make_transformed_item(
            collection_name=Constant.COLLECTION_NAME_POST,
            updated_object_list=[self._build_post_updated_object(collected_data)])
        )
        transformed_data.append(self._make_transformed_item(
            collection_name=Constant.COLLECTION_NAME_REPORT,
            updated_object_list=[self._build_report_updated_object(collected_data, loaded_item)])
        )
        transformed_data.append(self._make_transformed_item(
            collection_name=Constant.COLLECTION_NAME_MEDIA,
            updated_object_list=self._build_media_updated_objects(collected_data))
        )
        if collected_data.get('user'):
            _, collected_user_schema_error = self._validate_schema(data=collected_data['user'], schema=UserObjectSchema)
            if not collected_user_schema_error:
                transformed_data.append(self._make_transformed_item(
                    collection_name=Constant.COLLECTION_NAME_KOL,
                    updated_object_list=[self._build_kol_updated_object(collected_data)])
                )
                transformed_data.append(self._make_transformed_item(
                    collection_name=Constant.COLLECTION_NAME_USER,
                    updated_object_list=[self._build_user_updated_object(collected_data)])
                )
            else:
                self.logger.warning(f'User transform schema error {collected_user_schema_error}')
        return transformed_data

    def _build_post_updated_object(self, collected_data):
        post_stored_object_builder = StoredObjectBuilder()
        post_stored_object_builder.set_get_all_fields_from_collected_object('collected_post',
                                                                            excluded_fields='display_url')
        post_stored_object_builder.add_mapping('collected_user', {'_id': 'user_id'})

        post_stored_object = post_stored_object_builder.build(collected_post=collected_data['post'],
                                                              collected_user=collected_data.get('user'))

        post_stored_object['display_url'] = Common.md5_hash(collected_data['post']['display_url'])

        post_updated_object = self._make_updated_object(
            filter_={'_id': post_stored_object['_id']},
            stored_object=post_stored_object,
            upsert=True
        )

        return post_updated_object

    def _build_user_updated_object(self, collected_data):
        user_stored_object_builder = StoredObjectBuilder()
        user_stored_object_builder.set_get_all_fields_from_collected_object('collected_user',
                                                                            excluded_fields='avatar')

        user_stored_object = user_stored_object_builder.build(collected_user=collected_data['user'])

        user_stored_object['avatar'] = Common.md5_hash(collected_data['user']['avatar'])

        user_updated_object = self._make_updated_object(
            filter_={'_id': user_stored_object['_id']},
            stored_object=user_stored_object,
            upsert=True
        )
        return user_updated_object

    def _build_kol_updated_object(self, collected_data):
        kol_stored_object_builder = StoredObjectBuilder()
        kol_stored_object_builder.add_mapping('collected_user', {'_id': 'user_id', 'username': 'username'})

        kol_stored_object = kol_stored_object_builder.build(collected_user=collected_data.get('user'),
                                                            )
        kol_updated_object = self._make_updated_object(
            filter_={'username': kol_stored_object['username']},
            stored_object=kol_stored_object,
            upsert=False
        )

        return kol_updated_object

    def _build_media_updated_objects(self, collected_data) -> list:
        media_updated_objects = []

        if collected_data.get('post', {}).get('display_url'):
            media_updated_objects.append(
                self._build_media_updated_object(item_having_media=collected_data['post'],
                                                 mapping={'display_url': 'link'}))

        if collected_data.get('user', {}).get('avatar'):
            media_updated_objects.append(
                self._build_media_updated_object(item_having_media=collected_data['user'],
                                                 mapping={'avatar': 'link'}))

        return media_updated_objects

    def _build_media_updated_object(self, item_having_media, mapping):

        media_stored_object_builder = StoredObjectBuilder()
        media_stored_object_builder.add_mapping('item', mapping)
        media_stored_object = media_stored_object_builder.build(item=item_having_media)
        media_stored_object['_id'] = Common.md5_hash(media_stored_object['link'])
        media_stored_object['type'] = "Image"
        return self._make_updated_object(
            filter_={'_id': media_stored_object['_id']},
            stored_object=media_stored_object,
            upsert=True

        )

    def _build_report_updated_object(self, collected_data, loaded_item):

        today_date = self.now.strftime("%Y-%m-%d")

        report_statuses = self._build_report_statuses_object()
        report_builder = StoredObjectBuilder()

        report_builder.add_mapping('history_report',
                                   {f'history_report.{today_date}': 'history_report'
                                    })
        report_builder.add_mapping('collected_post',
                                   {'_id': 'post_id',
                                    'shortcode': 'shortcode'
                                    })
        report_builder.add_mapping('collected_user',
                                   {'username': 'username',
                                    '_id': 'user_id'})

        report_builder.set_get_all_fields_from_collected_object('report_statuses', None)

        report_stored_object = report_builder.build(
            report_statuses=report_statuses,
            collected_post=collected_data['post'],
            collected_user=collected_data.get('user'),

        )
        report_stored_object['_id'] = loaded_item['_id']
        report_stored_object[f'history_report.{today_date}'] = self._build_history_report_object(collected_data)
        report_stored_object['response_server.num_update'] = 0
        report_stored_object['tracking_status'] = 'Pending'
        report_updated_object = self._make_updated_object(
            filter_={'_id': loaded_item['_id']},
            stored_object=report_stored_object,
            upsert=False
        )
        report_stored_object['comment_report_status.status'] = 'new'

        return report_updated_object

    def _build_history_report_object(self, collected_data):
        today_report_history_builder = StoredObjectBuilder()
        today_report_history_builder.add_mapping('collected_post', {'num_like': 'num_like',
                                                                    'num_comment': 'num_comment',
                                                                    })
        today_report_history = today_report_history_builder.build(collected_post=collected_data['post'])
        today_report_history['taken_at_timestamp'] = int(self.now.timestamp())
        return today_report_history

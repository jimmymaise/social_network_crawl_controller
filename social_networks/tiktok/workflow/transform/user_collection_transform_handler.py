from config.system_config import SystemConfig
from core.handlers.file_handler.file_handler import FileHandler
from core.handlers.file_handler.s3_handler import S3Handler
from core.utils.exceptions import ErrorStoreFormat
from core.workflows.transform.base_item_transform_handler import BaseItemTransformHandler
from core.workflows.transform.stored_object.stored_object_builder import StoredObjectBuilder
from social_networks.tiktok.utils.constant import Constant
from social_networks.tiktok.workflow.transform.collected_object_schemas.collected_user_schema import UserObjectSchema


class UserCollectionTransformHandler(BaseItemTransformHandler):
    def __init__(self, service_name):
        super().__init__(service_name)
        self.s3_handler = S3Handler()

    def process_item(self, loaded_item, collected_data):
        transformed_data = []
        _, collected_user_schema_error = self._validate_schema(data=collected_data['user'], schema=UserObjectSchema)

        if collected_user_schema_error:
            raise ErrorStoreFormat(f'Schema error {str(collected_user_schema_error)}')

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

    def _build_user_updated_object(self, collected_data):
        user_stored_object_builder = StoredObjectBuilder()
        user_stored_object_builder.set_get_all_fields_from_collected_object('collected_user',
                                                                            excluded_fields='avatar')

        user_stored_object = user_stored_object_builder.build(collected_user=collected_data['user'])

        user_stored_object['avatar'] = self._get_image_id_from_social_url(url=collected_data['user']['avatar'])

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

        kol_stored_object = kol_stored_object_builder.build(collected_user=collected_data.get('user'),
                                                            report_statuses=self._build_kol_statuses_object()
                                                            )
        kol_updated_object = self._make_updated_object(
            filter_={'username': kol_stored_object['username']},
            stored_object=kol_stored_object,
            upsert=False
        )

        return kol_updated_object

    def _build_media_updated_objects(self, collected_data) -> list:
        media_updated_objects = []

        if collected_data.get('user', {}).get('avatar'):
            media_updated_objects.append(
                self._build_media_updated_object(item_having_media=collected_data['user'],
                                                 mapping={'avatar': 'link'}, media_type='avatar'))

        return media_updated_objects

import datetime
from abc import abstractmethod

from config.system_config import SystemConfig
from core.handlers.file_handler.file_handler import FileHandler
from core.handlers.file_handler.s3_handler import S3Handler
from core.logger.logger_handler import Logger
from core.workflows.transform.stored_object.stored_object_builder import StoredObjectBuilder


class BaseItemTransformHandler:
    @abstractmethod
    def __init__(self, service_name):
        self.logger = Logger.get_logger()
        self.service_name = service_name
        self.now = datetime.datetime.now()
        self.s3_handler = S3Handler()

    @abstractmethod
    def process_item(self, loaded_item, collected_data):
        pass

    @staticmethod
    def _validate_schema(data, schema):
        error = {}
        value = data
        try:
            value = dict(schema().load(data))
        except Exception as e:
            error = e
        return value, error

    @staticmethod
    def _make_updated_object(filter_, stored_object, upsert=True):
        return {
            'filter': filter_,
            'update': stored_object,
            'upsert': upsert,

        }

    @staticmethod
    def _make_transformed_item(collection_name: str, updated_object_list: list):
        return {
            'collection_name': collection_name,
            'items': updated_object_list
        }

    @staticmethod
    def _get_image_id_from_social_url(url):
        return FileHandler.get_file_name_from_url(url=url, is_have_extension=False)

    def _build_report_statuses_object(self):

        report_statuses_object = {
            f'{self.service_name}_status': {'status': 'success',
                                            'latest_updated_time': int(self.now.timestamp())
                                            },
            'response_server.is_update_report': True,
            'response_server.num_update': 0,
        }
        return report_statuses_object

    def _build_kol_statuses_object(self):

        report_statuses_object = {
            f'{self.service_name}_status': {'status': 'success',
                                            'latest_updated_time': int(self.now.timestamp())
                                            },
            'response_server.num_update': 0,
        }
        return report_statuses_object

    def _build_media_updated_object(self, item_having_media, mapping, media_type):
        media_stored_object_builder = StoredObjectBuilder()
        media_stored_object_builder.add_mapping('item', mapping)
        media_stored_object = media_stored_object_builder.build(item=item_having_media)
        media_stored_object['link'] = self.s3_handler.copy_file_from_external_url_to_s3(
            external_url=media_stored_object['link'],
            bucket=SystemConfig.S3_BUCKET_NAME,
            s3_folder_path=f'{SystemConfig.S3_IMAGE_PATH}/{media_type}'
        )
        media_stored_object['_id'] = self._get_image_id_from_social_url(url=media_stored_object['link'])
        return self._make_updated_object(
            filter_={'_id': media_stored_object['_id']},
            stored_object=media_stored_object,
            upsert=True)

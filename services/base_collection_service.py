import time
from abc import abstractmethod

from config.system_config import SystemConfig
from core.handlers.db_handler.base_db_handler import DBConnection
from core.handlers.db_handler.base_db_handler import GeneralDBHandler


class CollectionService:
    def __init__(self, service_config: dict):
        self.service_name = None
        self.system_config = SystemConfig
        self.service_config = service_config
        self.db_connection = self._create_db_connection_by_system_config()
        self.running_status = {

        }

    def _update_failed_status(self, load_id, error_code):
        self._store_data([
            {'collection_name': 'report',
             'items': [
                 {
                     'filter': {'_id': load_id},
                     'update': {
                         f'{self.service_name}_status': {'status': error_code,
                                                         'latest_updated_time': int(time.time())
                                                         },
                         'response_server.is_update_report': True,
                         'response_server.num_update': 0,
                     }
                 }
             ]
             }]
        )

    def _create_db_connection_by_system_config(self):
        self.mongodb_credential = {
            'db_username': SystemConfig.MONGO_DB_HOST,
            'db_name': SystemConfig.MONGO_DB_DATABASE_NAME,
            'db_password': SystemConfig.MONGO_DB_PASSWORD,
            'db_host': SystemConfig.MONGO_DB_HOST,
            'db_port': SystemConfig.MONGO_DB_PORT
        }
        return DBConnection(**self.mongodb_credential)

    @abstractmethod
    def _load_items(self) -> list:
        # Play something with self.loads to get data
        pass

    @abstractmethod
    def _collect_data(self, loaded_items: list):
        # Play something with self.collect_handler to get data
        pass

    @abstractmethod
    def _transform_data(self, loaded_item, collected_data):
        # Play something with self.item_transform
        pass

    def _store_data(self, transformed_data):
        for obj in transformed_data:
            GeneralDBHandler(collection_name=obj['name'], connection=self.db_connection). \
                bulk_write_many_update_objects(obj['items'])

    def process(self):
        loaded_items = self._load_items()
        for loaded_item in loaded_items:
            try:
                collected_data = self._collect_data(loaded_item)
                transformed_data = self._transform_data(loaded_item, collected_data)
                self._store_data(transformed_data)
            except Exception as e:
                error_code = getattr(e, 'collection_service_error_name', 'error_unknown')
                self._update_failed_status(load_id=loaded_item['_id'], error_code=error_code)

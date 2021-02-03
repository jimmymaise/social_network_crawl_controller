import time
from abc import abstractmethod

from config.system_config import SystemConfig
from core.handlers.db_handler.base_db_handler import DBConnection
from core.handlers.db_handler.base_db_handler import GeneralDBHandler
from core.utils.constant import Constant


class CollectionService:
    def __init__(self, service_config: dict, collection_report_name: str):
        self.service_name = None
        self.system_config = SystemConfig
        self.service_config = service_config
        self.db_connection = self._create_db_connection_by_system_config()
        self.logger = None
        self.collection_report_name = collection_report_name

    def _update_failed_status(self, load_id, exception):
        error_code = getattr(exception, Constant.COLLECTION_SERVICE_ERROR_NAME, Constant.DEFAULT_UNKNOWN_ERROR_CODE)
        self.logger.error(exception, exc_info=True)

        self._store_data([
            {'collection_name': self.collection_report_name,
             'items': [
                 {
                     'filter': {'_id': load_id},
                     'update': {
                         f'{self.service_name}_status': {'status': error_code,
                                                         'exception_detail': str(exception),
                                                         'latest_updated_time': int(time.time())
                                                         },
                     }
                 }
             ]
             }]
        )

    def _create_db_connection_by_system_config(self):
        self.mongodb_credential = {
            'db_username': SystemConfig.MONGO_DB_USERNAME,
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

    def _store_data(self, transformed_data, **kwargs):
        for obj in transformed_data:
            GeneralDBHandler(collection_name=obj['collection_name'], connection=self.db_connection). \
                bulk_write_many_update_objects(obj['items'])

    def _process(self):
        loaded_items = self._load_items()
        self.logger.info(f'Load {len(loaded_items)} item for {self.service_name}')
        for loaded_item in loaded_items:
            try:
                collected_data = self._collect_data(loaded_item)
                transformed_data = self._transform_data(loaded_item, collected_data)
                self._store_data(transformed_data)
                self.logger.info(f'Load Item Id {loaded_item["_id"]} successful!')

            except Exception as e:
                self.logger.error(f'Load Item Id {loaded_item["_id"]}, Error: {e}')
                self._update_failed_status(load_id=loaded_item['_id'], exception=e)

    def start(self):
        self.logger.info(f'Starting service {self.service_name}')
        while True:
            self._process()
            time.sleep(int(SystemConfig.SERVICE_SLEEP_INTERVAL))
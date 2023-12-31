import time
from abc import ABC
from abc import abstractmethod

from bson.objectid import ObjectId

from config.system_config import SystemConfig
from core.handlers.db_handler.base_db_handler import DBConnection
from core.handlers.db_handler.base_db_handler import GeneralDBHandler
from core.handlers.on_demand_handler.on_demand_handler import OnDemandHandler
from core.handlers.queue_handler.sqs_handler import SQSHandler
from core.logger.logger_handler import Logger
from core.utils.common import Common
from core.utils.constant import Constant


class CollectionService(ABC):
    def __init__(self, service_config: dict, loaded_collection_name: str, service_name: str,
                 error_key='_id', on_demand_handler: OnDemandHandler = None):
        self.service_name = service_name
        self.on_demand_handler = on_demand_handler
        self.system_config = SystemConfig.get_system_config()
        self.service_config = service_config
        self.db_connection = self._create_db_connection_by_system_config()
        self.logger = Logger().init_logger(logger_name=f'{self.system_config.SOCIAL_NETWORK}-{self.service_name}')
        self.receive_message_schema = None
        self.loaded_item_message_mapping = None
        self.loaded_collection_name = loaded_collection_name
        self.is_on_demand = bool(on_demand_handler)
        self.sqs_handler = SQSHandler()
        self.error_key = error_key

    def _update_failed_status(self, load_id, exception):
        error_code = getattr(exception, Constant.COLLECTION_SERVICE_ERROR_NAME, Constant.DEFAULT_UNKNOWN_ERROR_CODE)
        self.logger.error(exception, exc_info=True)

        self._store_data_to_db([
            {'collection_name': self.loaded_collection_name,
             'items': [
                 {
                     'filter': {self.error_key: load_id},
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
            'db_username': self.system_config.MONGO_DB_USERNAME,
            'db_name': self.system_config.MONGO_DB_DATABASE_NAME,
            'db_password': self.system_config.MONGO_DB_PASSWORD,
            'db_host': self.system_config.MONGO_DB_HOST,
            'db_port': self.system_config.MONGO_DB_PORT
        }
        return DBConnection(**self.mongodb_credential)

    def _load_item_from_message(self):
        if not self.on_demand_handler:
            raise Exception('NotSupportOnDemandMode')

        item = self.on_demand_handler.message

        if not (self.loaded_item_message_mapping and self.receive_message_schema and self.loaded_collection_name):
            raise Exception('Must have loaded_item_message_mapping,receive_message_schema and loaded_collection_name')

        _, error = Common.validate_schema(item, self.receive_message_schema)
        if error:
            raise Exception(f'Message error {error}')

        item = Common.transform_dict_with_mapping(item, self.loaded_item_message_mapping)

        if not item['_id'] and self.loaded_item_message_mapping['_id'] == 'ObjectId()':
            item['_id'] = ObjectId()

        return item

    @abstractmethod
    def _load_items_from_db(self) -> list:
        # Play something with self.loads to get data
        pass

    def _load_items_from_db_for_sqs(self, loaded_item) -> list:
        # Play something with self.loads to get data
        return [loaded_item]

    @abstractmethod
    def _collect_data(self, loaded_items: list):
        # Play something with self.collect_handler to get data
        pass

    @abstractmethod
    def _transform_data(self, loaded_item, collected_data):
        # Play something with self.item_transform
        pass

    def _store_data_to_db(self, transformed_data, **kwargs):

        for obj in transformed_data:
            GeneralDBHandler(collection_name=obj['collection_name'], connection=self.db_connection). \
                bulk_write_many_update_objects(obj['items'])

    def _sync_data_to_sqs(self, loaded_item, transformed_data):
        # Sync data to sqs
        pass

    def _on_demand_process(self):
        loaded_item = self._load_item_from_message()
        loaded_items = self._load_items_from_db_for_sqs(loaded_item)
        self._base_process(loaded_items)

    def _scheduler_process(self):
        loaded_items = self._load_items_from_db()
        self._base_process(loaded_items)

    def _base_process(self, loaded_items):
        self.logger.info(f'Load {len(loaded_items)} item for {self.service_name}')
        for loaded_item in loaded_items:
            try:
                collected_data = self._collect_data(loaded_item)
                transformed_data = self._transform_data(loaded_item, collected_data)
                self._store_data_to_db(transformed_data)
                self._sync_data_to_sqs(loaded_item, transformed_data)
                self.logger.info(f'Load Item Id {loaded_item["_id"]} successful!')
            except Exception as e:
                self.logger.error(f'Load Item Id {loaded_item["_id"]}, Error: {e}')
                if self.is_on_demand:
                    raise Exception(e)
                self._update_failed_status(load_id=loaded_item['_id'], exception=e)

    def start(self):
        self.logger.info(f'Starting service {self.service_name}')

        if self.is_on_demand:
            self._on_demand_process()
            return

        while True:
            self._scheduler_process()
            time.sleep(int(self.system_config.SERVICE_SLEEP_INTERVAL))

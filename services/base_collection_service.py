from abc import abstractmethod

from config.system_config import SystemConfig
from core.handlers.db_handler.base_db_handler import DBConnection


class CollectionService:
    def __init__(self, service_config: dict):
        self.service_name = None
        self.system_config = SystemConfig
        self.service_config = service_config
        self.db_connection = self._create_db_connection_by_system_config()

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

    @abstractmethod
    def _store_data(self, transformed_data):
        pass

    def process(self):
        loaded_items = self._load_items()
        for loaded_item in loaded_items:
            collected_data = self._collect_data(loaded_item)
            transformed_data = self._transform_data(loaded_item, collected_data)
            self._store_data(transformed_data)

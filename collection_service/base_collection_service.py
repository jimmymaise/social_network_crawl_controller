from abc import abstractmethod

from collection_loading.load.base_load_handler import BaseLoadHandler


class CollectionService:
    def __init__(self, loader: BaseLoadHandler, collect_handler,
                 item_transform):
        self.loader = loader
        self.collect_handler = collect_handler
        self.item_transform = item_transform
        self.service_name = None

    @abstractmethod
    def _load_items(self) -> list:
        # Play something with self.loads to get data
        pass

    @abstractmethod
    def _get_crawl_data(self, loaded_items: list) -> list:
        # Play something with self.collect_handler to get data
        pass

    @abstractmethod
    def _prepare_data_for_storing(self, loaded_items, crawled_items):
        # Play something with self.item_transform
        pass

    @abstractmethod
    def _store_to_database(self, data):
        pass

    def process(self):
        loaded_items = self._load_items()
        crawled_items = self._get_crawl_data(loaded_items)
        data = self._prepare_data_for_storing(loaded_items, crawled_items)
        self._store_to_database(data)

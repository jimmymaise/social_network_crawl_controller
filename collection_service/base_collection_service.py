from abc import abstractmethod


class CollectionService:
    def __init__(self):
        self.service_name = None

    @abstractmethod
    def _load_items(self) -> list:
        # Play something with self.loads to get data
        pass

    @abstractmethod
    def _collect_data(self, loaded_items: list) -> list:
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

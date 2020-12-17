from abc import ABCMeta, abstractmethod

from collection_loading.query.base_query import Query


class BaseLoadHandler(object, metaclass=ABCMeta):
    def __init__(self, db_handler):
        self.load_collection_name = None
        self.items = []
        self.filters = []
        self.db_handler = db_handler

    def add_filter(self, _filter: Query):
        self.filters.append(_filter)

    def _get_items_from_filter(self, _filter: Query) -> list:
        return self.db_handler.get_items_by_filter(_filter, self.load_collection_name)

    def load_items(self):
        if not self.filters:
            raise Exception('Need to have filters')
        if not self.items:
            for _filter in self.filters:
                self.items += self._get_items_from_filter(_filter)
        return self.items

from abc import ABCMeta, abstractmethod

from collection_loading.query.base_query import Query


class BaseLoadHandler(object, metaclass=ABCMeta):
    def __init__(self, db_handler):
        self.load_collection_name = None
        self.items = []
        self.queries = []
        self.db_handler = db_handler

    def add_query(self, query: Query):
        self.queries.append(query)

    def _get_items_from_query(self, query: Query) -> list:
        return self.db_handler.get_items_by_query(query, self.load_collection_name)

    def load_items(self):
        if not self.queries:
            raise Exception('Need to have filters')
        if not self.items:
            for query in self.queries:
                self.items += self._get_items_from_query(query)
        return self.items

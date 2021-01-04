from abc import ABCMeta, abstractmethod

from workflow.loading.query.base_query import Query


class BaseLoadHandler(object, metaclass=ABCMeta):
    def __init__(self, db_handler):
        self.load_collection_name = None
        self.items = []
        self.queries = []
        self.db_handler = db_handler

    def add_query(self, query: Query):
        self.queries.append(query)

    @abstractmethod
    def _get_items_from_query(self, query: Query) -> list:
        pass

    def load_items(self):
        if not self.queries:
            raise Exception('Need to have filters')
        if not self.items:
            for query in self.queries:
                self.items += self._get_items_from_query(query)
        return self.items

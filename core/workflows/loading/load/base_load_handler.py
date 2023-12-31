from abc import ABCMeta

from core.logger.logger_handler import Logger
from core.workflows.loading.query.base_query import Query, Aggregate


class BaseLoadHandler(object, metaclass=ABCMeta):
    def __init__(self, db_handler):
        self.load_collection_name = None
        self.items = []
        self.queries = []
        self.db_handler = db_handler
        self.logger = Logger.get_logger()

    def add_query(self, query: Query):
        self.queries.append(query)

    def aggregate(self, query: Aggregate):
        return self.db_handler.aggregate(query.build())

    def _get_items_from_query(self, query: Query):
        return self.db_handler.get_many_by_filter(
            filter_=query.filter_,
            sort_=query.sort_,
            limit=query.limit,
            selected_fields=query.selected_fields
        )

    def load_items(self):
        if not self.queries:
            raise Exception('Need to have filters')
        if not self.items:
            for query in self.queries:
                self.items += self._get_items_from_query(query)
        return self.items

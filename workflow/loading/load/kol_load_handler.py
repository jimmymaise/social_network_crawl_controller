from workflow.loading.load.base_load_handler import BaseLoadHandler
from workflow.loading.query.base_query import Query
from core.handlers.db_handler.kol_db_handler import KOLDBHandler


class KOLLoadHandler(BaseLoadHandler):
    def __init__(self, db_handler: KOLDBHandler):
        super(KOLLoadHandler, self).__init__(db_handler)

    def _get_items_from_query(self, query: Query):
        return self.db_handler.get_many_by_filter_and_sort(
            filter_=query.filter_,
            sort_=query.sort_,
            limit_=query.limit_,
            selected_fields_=query.selected_fields_
        )

from core.handlers.db_handler.kol_db_handler import KOLDBHandler
from workflow.loading.load.base_load_handler import BaseLoadHandler


class KOLLoadHandler(BaseLoadHandler):
    def __init__(self, db_handler: KOLDBHandler):
        super(KOLLoadHandler, self).__init__(db_handler)
        self.load_collection_name = 'kols'

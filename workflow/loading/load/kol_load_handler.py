from core.handlers.db_handler.kol_db_handler import KOLDBHandler
from core.utils.constant import Constant
from workflow.loading.load.base_load_handler import BaseLoadHandler


class KOLLoadHandler(BaseLoadHandler):
    def __init__(self, db_handler: KOLDBHandler):
        super().__init__(db_handler)
        self.load_collection_name = Constant.COLLECTION_NAME_KOL

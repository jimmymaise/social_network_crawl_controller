from core.workflows.loading.load.base_load_handler import BaseLoadHandler
from social_networks.facebook.handlers.db_handler.kol_db_handler import KOLDBHandler
from social_networks.facebook.utils.constant import Constant


class KOLLoadHandler(BaseLoadHandler):
    def __init__(self, db_handler: KOLDBHandler):
        super().__init__(db_handler)
        self.load_collection_name = Constant.COLLECTION_NAME_KOL

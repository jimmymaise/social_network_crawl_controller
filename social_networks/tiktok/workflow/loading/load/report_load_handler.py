from core.workflows.loading.load.base_load_handler import BaseLoadHandler
from social_networks.tiktok.utils.constant import Constant


class ReportLoadHandler(BaseLoadHandler):
    def __init__(self, db_handler):
        super().__init__(db_handler)
        self.load_collection_name = Constant.COLLECTION_NAME_REPORT

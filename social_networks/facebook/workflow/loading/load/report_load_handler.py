from social_networks.facebook.utils.constant import Constant
from core.workflows.loading.load.base_load_handler import BaseLoadHandler


class ReportLoadHandler(BaseLoadHandler):
    def __init__(self, db_handler):
        super().__init__(db_handler)
        self.load_collection_name = Constant.COLLECTION_NAME_REPORT

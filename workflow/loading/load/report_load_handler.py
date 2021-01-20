from core.utils.constant import Constant
from workflow.loading.load.base_load_handler import BaseLoadHandler


class ReportLoadHandler(BaseLoadHandler):
    def __init__(self, db_handler):
        super().__init__(db_handler)
        self.load_collection_name = Constant.COLLECTION_NAME_REPORT

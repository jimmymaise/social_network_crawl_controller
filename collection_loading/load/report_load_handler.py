from collection_loading.load.base_load_handler import BaseLoadHandler


class ReportLoadHandler(BaseLoadHandler):
    def __init__(self, db_handler):
        super(ReportLoadHandler, self).__init__(db_handler)
        self.load_collection_name = 'reports'

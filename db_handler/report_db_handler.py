from db_handler.base_db_handler import BaseDBHandler


class ReportDBHandler(BaseDBHandler):
    def __init__(self):
        super(ReportDBHandler, self).__init__()
        self.collection = self.database['reports']

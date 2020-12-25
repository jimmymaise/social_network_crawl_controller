from db_handler import general_db_handler


class ReportDBHandler(general_db_handler):
    def __init__(self):
        super(ReportDBHandler, self).__init__()
        self.collection = self.database['reports']

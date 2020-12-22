from DBService.DBHandler.GeneralDBHandler import GeneralDBHandler


class ReportDBHandler(GeneralDBHandler):
    def __init__(self):
        super(ReportDBHandler, self).__init__()
        self.collection = self.database['reports']

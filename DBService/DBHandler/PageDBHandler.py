from DBService.DBHandler.GeneralDBHandler import GeneralDBHandler

class PageDBHandler(GeneralDBHandler):
    def __init__(self):
        super(PageDBHandler, self).__init__()
        self.collection = self.database['pages']
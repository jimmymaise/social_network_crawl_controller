from db_handler import general_db_handler


class PageDBHandler(general_db_handler):
    def __init__(self):
        super(PageDBHandler, self).__init__()
        self.collection = self.database['pages']
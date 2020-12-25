from db_handler.base_db_handler import BaseDBHandler


class PageDBHandler(BaseDBHandler):
    def __init__(self):
        super(PageDBHandler, self).__init__()
        self.collection = self.database['pages']
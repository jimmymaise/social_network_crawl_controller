from db_handler.base_db_handler import BaseDBHandler


class WatcherDBHandler(BaseDBHandler):
    def __init__(self):
        super(WatcherDBHandler, self).__init__()
        self.collection = self.database['watchers']

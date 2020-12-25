from db_handler import general_db_handler


class WatcherDBHandler(general_db_handler):
    def __init__(self):
        super(WatcherDBHandler, self).__init__()
        self.collection = self.database['watchers']

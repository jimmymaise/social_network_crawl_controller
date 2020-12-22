from DBService.DBHandler.GeneralDBHandler import GeneralDBHandler


class WatcherDBHandler(GeneralDBHandler):
    def __init__(self):
        super(WatcherDBHandler, self).__init__()
        self.collection = self.database['watchers']

from DBService.DBHandler.GeneralDBHandler import GeneralDBHandler


class PostReactionDBHandler(GeneralDBHandler):
    def __init__(self):
        super(PostReactionDBHandler, self).__init__()
        self.collection = self.database['postreactions']

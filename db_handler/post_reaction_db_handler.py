from db_handler import general_db_handler


class PostReactionDBHandler(general_db_handler):
    def __init__(self):
        super(PostReactionDBHandler, self).__init__()
        self.collection = self.database['postreactions']

from db_handler.base_db_handler import BaseDBHandler


class PostReactionDBHandler(BaseDBHandler):
    def __init__(self):
        super(PostReactionDBHandler, self).__init__()
        self.collection = self.database['postreactions']

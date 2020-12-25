from db_handler.base_db_handler import BaseDBHandler


class UserFollowUserDBHandler(BaseDBHandler):
    def __init__(self):
        super(UserFollowUserDBHandler, self).__init__()
        self.collection = self.database['userfollowusers']

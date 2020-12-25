from db_handler import general_db_handler


class UserFollowUserDBHandler(general_db_handler):
    def __init__(self):
        super(UserFollowUserDBHandler, self).__init__()
        self.collection = self.database['userfollowusers']

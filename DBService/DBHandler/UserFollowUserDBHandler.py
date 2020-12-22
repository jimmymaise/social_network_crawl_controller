from DBService.DBHandler.GeneralDBHandler import GeneralDBHandler


class UserFollowUserDBHandler(GeneralDBHandler):
    def __init__(self):
        super(UserFollowUserDBHandler, self).__init__()
        self.collection = self.database['userfollowusers']

# Import DBHandler
from DBService.DBHandler.PostReactionDBHandler import PostReactionDBHandler


class PostReactionService(object):
    # ********** Constructor **********
    def __init__(self):
        self.postreaction_dbhandler = PostReactionDBHandler()

    # ********** Get all reaction of a post **********
    def get_all_reaction_of_post(self,
                                 _post_id):
        result = self.postreaction_dbhandler.get_many_by_filter(_filter={'post_id': _post_id})

        # ===== Return value =====
        return result

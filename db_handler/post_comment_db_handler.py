from pymongo import UpdateOne
from db_handler.base_db_handler import BaseDBHandler


class PostCommentDBHandler(BaseDBHandler):
    def __init__(self):
        super(PostCommentDBHandler, self).__init__()
        self.collection = self.database['postcomments']

    def update_post_comment(self, list_post_comment):
        """
        Update list "post comment" for post after crawled
        """
        if list_post_comment and isinstance(list_post_comment, list):
            list_cmt_obj = [UpdateOne(cmt_filter, {"$set": _updated_record}, upsert=True)\
                            for cmt_filter, _updated_record in list_post_comment]
            reuslt = self.collection.bulk_write(list_cmt_obj)
            return reuslt
        else:
            return False
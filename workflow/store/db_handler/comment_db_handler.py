from pymongo import UpdateOne
from workflow.store.db_handler import BaseDBHandler


class CommentDBHandler(BaseDBHandler):
    def __init__(self):
        super(CommentDBHandler, self).__init__()
        self.collection = self.database['comments']

    def get_comments_by_post_id(self,
                                _post_id,
                                _selected_fields=None):
        # ===== Execute =====
        result = self.get_many_by_filter(_filter={'post_id': _post_id},
                                         _selected_fields=_selected_fields)
        return result

    def update_comment(self, list_comment):
        """
        Update list "comment" for post after crawled
        """
        if list_comment and isinstance(list_comment, list):
            list_cmt_obj = [UpdateOne(cmt_filter, {"$set": _updated_record}, upsert=True)\
                            for cmt_filter, _updated_record in list_comment]
            reuslt = self.collection.bulk_write(list_cmt_obj)
            return reuslt
        else:
            return False

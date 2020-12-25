# Import libs
from db_handler.base_db_handler import BaseDBHandler


class NormalUserDBHandler(BaseDBHandler):
    def __init__(self):
        super(NormalUserDBHandler, self).__init__()
        self.collection = self.database['normalusers']

    def get_one_by_user_id(self,
                           _user_id,
                           _selected_fields=None):
        # ===== Execute =====
        result = self.get_one_by_filter(_filter={'user_id': _user_id},
                                        _selected_fields=_selected_fields)
        return result

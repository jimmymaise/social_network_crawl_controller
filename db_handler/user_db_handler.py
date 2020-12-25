from db_handler.base_db_handler import BaseDBHandler


class UserDBHandler(BaseDBHandler):
    def __init__(self):
        super(UserDBHandler, self).__init__()
        self.collection = self.database['users']

    def get_one_by_user_id(self,
                           _user_id,
                           _selected_fields=None):
        # ===== Execute =====
        result = self.get_one_by_filter(_filter={'_id': _user_id},
                                        _selected_fields=_selected_fields)
        return result

    def get_one_by_app_id(self,
                          _app_id,
                          _selected_fields=None):
        # ===== Execute =====
        result = self.get_one_by_filter(_filter={'_id': _app_id},
                                        _selected_fields=_selected_fields)
        return result

    def get_one_by_username(self,
                            _username,
                            _selected_fields=None):
        # ===== Execute =====
        found_user = self.get_one_by_filter(_filter={'username': _username},
                                            _selected_fields=_selected_fields)
        return found_user

# Import libs
from core.handlers.db_handler.base_db_handler import BaseDBHandler


class KOLDBHandler(BaseDBHandler):
    def __init__(self):
        super(KOLDBHandler, self).__init__()
        self.collection = self.database['kols']

    def get_one_by(self,
                   _hiip_user_id=None,
                   _hiip_user_type=None,
                   _country_code=None,
                   _selected_fields=None):
        result = None

        if _hiip_user_id and _hiip_user_type and _country_code:
            result = self.get_one_by_filter(_filter={'hiip_user_id': _hiip_user_id,
                                                     'hiip_user_type': _hiip_user_type,
                                                     'country_code': _country_code},
                                            _selected_fields=_selected_fields)

        return result

    def get_one_by_username(self,
                            _username,
                            _selected_fields=None):
        # ===== Execute =====
        result = self.get_one_by_filter(_filter={'username': _username},
                                        _selected_fields=_selected_fields)
        return result

    def get_one_by_user_id(self,
                           _user_id,
                           _selected_fields=None):
        # ===== Execute =====
        result = self.get_one_by_filter(_filter={'user_id': _user_id},
                                        _selected_fields=_selected_fields)
        return result

    def get_one_by_app_id(self,
                          _app_id,
                          _selected_fields=None):
        # ===== Execute =====
        result = self.get_one_by_filter(_filter={'app_id': _app_id},
                                        _selected_fields=_selected_fields)
        return result

    def get_many_pairs_by_user_id(self,
                                  _user_ids,
                                  _selected_fields=None):
        # ===== Execute =====
        result = self.get_many_by_filter(_filter={'user_id': {'$in': _user_ids}},
                                         _selected_fields=_selected_fields)
        return result

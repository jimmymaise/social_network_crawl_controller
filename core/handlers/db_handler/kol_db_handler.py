# Import libs
from core.handlers.db_handler.base_db_handler import BaseDBHandler
from core.utils.constant import Constant


class KOLDBHandler(BaseDBHandler):
    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.collection = self.database[Constant.COLLECTION_NAME_KOL]

    def get_one_by(self,
                   hiip_user_id=None,
                   hiip_user_type=None,
                   country_code=None,
                   selected_fields=None):
        result = None

        if hiip_user_id and hiip_user_type and country_code:
            result = self.get_one_by_filter(filter_={'hiip_user_id': hiip_user_id,
                                                     'hiip_user_type': hiip_user_type,
                                                     'country_code': country_code},
                                            selected_fields=selected_fields)

        return result

    def get_one_by_username(self,
                            _username,
                            selected_fields=None):
        # ===== Execute =====
        result = self.get_one_by_filter(filter_={'username': _username},
                                        selected_fields=selected_fields)
        return result

    def get_one_by_user_id(self,
                           _user_id,
                           selected_fields=None):
        # ===== Execute =====
        result = self.get_one_by_filter(filter_={'user_id': _user_id},
                                        selected_fields=selected_fields)
        return result

    def get_one_by_app_id(self,
                          _app_id,
                          selected_fields=None):
        # ===== Execute =====
        result = self.get_one_by_filter(filter_={'app_id': _app_id},
                                        selected_fields=selected_fields)
        return result

    def get_many_pairs_by_user_id(self,
                                  _user_ids,
                                  selected_fields=None):
        # ===== Execute =====
        result = self.get_many_by_filter(filter_={'user_id': {'$in': _user_ids}},
                                         selected_fields=selected_fields)
        return result

# Import libs
import time  # Time lib

# Import Models
from DBService.Models.CrawlStatusEnum import CrawlStatusEnum

# Import DBHandler
from DBService.DBHandler.KOLDBHandler import KOLDBHandler
from DBService.DBHandler.NormalUserDBHandler import NormalUserDBHandler


class NormalUserService(object):
    def __init__(self):
        self.kol_dbhandler = KOLDBHandler()
        self.normaluser_dbhandler = NormalUserDBHandler()

    # ********** Update profile info of Normal users **********
    def update_profile_info_users(self,
                                  _user_infos):
        _user_objs = []
        for _user_info in _user_infos:
            _user = _user_info['body']
            _new_record = {}
            if _user_info['code'] == 200:
                _new_record['crawl_profile_code'] = 200
                _new_record['username'] = _user['username']
                _user_objs.append([{'_id': _user['_id']},
                                   _new_record])
            else:
                _new_record['crawl_profile_code'] = _user_info['code']
                _user_objs.append([{'_id': _user['_id']},
                                   _new_record])

        service_result = self.normaluser_dbhandler.update_many_pair(_updated_records=_user_objs)

        # ===== Return value =====
        return service_result

    # ********** Get user(s) by user_id **********
    def get_user_by_user_id(self,
                            _user_id,
                            _selected_fields=None):
        result = self.normaluser_dbhandler.get_one_by_user_id(_user_id=_user_id,
                                                              _selected_fields=_selected_fields)
        return result

    # region Change Profile Status

    def _change_profile_status_to(self,
                                  _users,
                                  _profile_status,
                                  _save_current_time=False):
        if not _users:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _user in _users:
            _record = {'crawl_profile_status': _profile_status}
            if _save_current_time:
                _record['last_time_crawl_profile'] = _current_timestamp
            _updated_records.append([{'_id': _user['_id']},
                                     _record])
        service_result = self.normaluser_dbhandler.update_many_pair(_updated_records=_updated_records)

        if service_result:
            return service_result
        return 'success'

    # ********** Change crawl_profile_status of KOLs to Crawling **********
    def change_profile_status_to_crawling(self,
                                          _users):
        return self._change_profile_status_to(_users=_users,
                                              _profile_status=CrawlStatusEnum.Crawling)

    # ********** Change crawl_profile_status of KOLs to Crawled **********
    def change_profile_status_to_crawled(self,
                                         _users):
        return self._change_profile_status_to(_users=_users,
                                              _profile_status=CrawlStatusEnum.Crawled,
                                              _save_current_time=True)

    # ********** Change crawl_profile_status of KOLs to Recrawl **********
    def change_profile_status_to_recrawl(self,
                                         _users):
        return self._change_profile_status_to(_users=_users,
                                              _profile_status=CrawlStatusEnum.Recrawl,
                                              _save_current_time=True)

    # ********** Change crawl_profile_status of KOLs to Error **********
    def change_profile_status_to_error(self,
                                       _users):
        return self._change_profile_status_to(_users=_users,
                                              _profile_status=CrawlStatusEnum.Error,
                                              _save_current_time=True)

    # endregion

# Import libs
import time  # Time lib

# Import Models
from DBService.Models.CrawlStatusEnum import CrawlStatusEnum
from DBService.Models.DocStatusEnum import DocStatusEnum

# Import DBHandler
from DBService.DBHandler.KOLDBHandler import KOLDBHandler
from DBService.DBHandler.UserDBHandler import UserDBHandler
from DBService.DBHandler.MediaDBHandler import MediaDBHandler

# Import utils
from SuperUtils import DictHelper, DateHelper


class KOLService(object):
    def __init__(self):
        self.kol_dbhandler = KOLDBHandler()
        self.user_dbhandler = UserDBHandler()
        self.media_dbhandler = MediaDBHandler()

    # region Insert new KOL into table

    # ********** Insert new KOL **********
    def get_user_by(self,
                    _hiip_user_id=None,
                    _hiip_user_type=None,
                    _country_code=None,
                    _app_id=None,
                    _username=None,
                    _user_id=None,
                    _selected_fields=None):
        found_user = None

        if found_user is None and _hiip_user_id:
            found_user = self.kol_dbhandler.get_one_by(_hiip_user_id=_hiip_user_id,
                                                       _hiip_user_type=_hiip_user_type,
                                                       _country_code=_country_code,
                                                       _selected_fields=_selected_fields)

        if found_user is None and _user_id:
            found_user = self.kol_dbhandler.get_one_by_user_id(_user_id=_user_id,
                                                               _selected_fields=_selected_fields)

        if found_user is None and _app_id and int(_app_id) > 0:
            found_user = self.kol_dbhandler.get_one_by_app_id(_app_id=int(_app_id),
                                                              _selected_fields=_selected_fields)
        if found_user is None and _username:
            found_user = self.kol_dbhandler.get_one_by_username(_username=_username,
                                                                _selected_fields=_selected_fields)

        return found_user

    # endregion

    # region Get Users

    # ********** Get user(s) by id **********
    def get_user_by_id(self,
                       _id,
                       _selected_fields=None):
        service_result = self.kol_dbhandler.get_one_by_id(_id=_id, _selected_fields=_selected_fields)
        return service_result

    def get_users_by_id(self,
                        _ids,
                        _selected_fields=None):
        service_result = self.kol_dbhandler.get_many_pairs_by_id(_ids=_ids, _selected_fields=_selected_fields)
        return service_result

    # ********** Get user(s) by user_id **********
    def get_user_by_user_id(self,
                            _user_id,
                            _selected_fields=None):
        if _user_id == -1:
            return None

        service_result = self.kol_dbhandler.get_one_by_user_id(_user_id=_user_id,
                                                               _selected_fields=_selected_fields)
        return service_result

    def get_users_by_user_id(self,
                             _user_ids,
                             _selected_fields=None):
        service_result = self.kol_dbhandler.get_many_pairs_by_user_id(_user_ids=_user_ids,
                                                                      _selected_fields=_selected_fields)
        return service_result

    # endregion

    # region Get Users to Crawl their Identity

    # ********** Get KOLs where crawl_identity_status is Not Exist **********
    def get_not_exist_identity_status_users(self,
                                            _num_user=150):
        result = self.kol_dbhandler.get_many_by_filter({'crawl_identity_status': {'$exists': False}
                                                        }).limit(_num_user)
        return result

    # ********** Get KOLs where crawl_identity_status is Created **********
    def get_created_identity_status_users(self,
                                          _num_user=150):
        result = self.kol_dbhandler.get_many_by_filter({'$and': [{'crawl_identity_status': {'$exists': True}},
                                                                 {'crawl_identity_status': CrawlStatusEnum.Created}]
                                                        }).limit(_num_user)
        return result

    # ********** Get KOLs where crawl_identity_status is Pending **********
    def get_pending_identity_status_users(self,
                                          _num_user=150):
        result = self.kol_dbhandler.get_many_by_filter({'crawl_identity_status': CrawlStatusEnum.Pending}).limit(
            _num_user)
        return result

    # ********** Get KOLs where crawl_identity_status is Crawled **********
    def get_crawled_identity_status_users(self,
                                          _num_user=150,
                                          _duration_refresh=43200):
        _current_timestamp = time.time()
        _last_timestamp = _current_timestamp - _duration_refresh
        result = self.kol_dbhandler.get_many_by_filter({'crawl_identity_status': CrawlStatusEnum.Crawled,
                                                        '$or': [{'last_time_crawl_identity': {'$exists': False}},
                                                                {'$and': [
                                                                    {'last_time_crawl_identity': {'$exists': True}},
                                                                    {'last_time_crawl_identity': {
                                                                        '$lt': _last_timestamp}}]
                                                                }
                                                                ]
                                                        }).limit(_num_user)
        return result

    # endregion

    # region Get Users to Crawl Their Profile

    # ********** Get KOLs where crawl_profile_status is Pending **********
    def get_pending_profile_status_users(self,
                                         _num_user=150):
        result = self.kol_dbhandler.get_many_by_filter({'crawl_identity_status': CrawlStatusEnum.Crawled,
                                                        'crawl_profile_status': CrawlStatusEnum.Pending
                                                        }).limit(_num_user)
        return result

    # ********** Get KOLs where crawl_profile_status is Not Exist **********
    def get_not_exist_profile_status_users(self,
                                           _num_user=150):
        result = self.kol_dbhandler.get_many_by_filter({'crawl_identity_status': CrawlStatusEnum.Crawled,
                                                        'crawl_profile_status': {'$exists': False}
                                                        }).limit(_num_user)
        return result

    # ********** Get KOLs where crawl_profile_status is Created **********
    def get_created_profile_status_users(self,
                                         _num_user=150):
        result = self.kol_dbhandler.get_many_by_filter({'crawl_identity_status': CrawlStatusEnum.Crawled,
                                                        'fb_user_type': 'user',
                                                        '$and': [{'crawl_profile_status': {'$exists': True}},
                                                                 {'crawl_profile_status': CrawlStatusEnum.Created}
                                                                 ]
                                                        }).limit(_num_user)
        return result

    # ********** Get KOLs where crawl_profile_status is Crawled **********
    def get_crawled_profile_status_users(self,
                                         _num_user=150,
                                         _duration_refresh=43200):
        _current_timestamp = time.time()
        _last_timestamp = _current_timestamp - _duration_refresh
        result = self.kol_dbhandler.get_many_by_filter({'crawl_profile_status': CrawlStatusEnum.Crawled,
                                                        '$or': [{'last_time_crawl_profile': {'$exists': False}},
                                                                {'last_time_crawl_profile': {'$lt': _last_timestamp}}
                                                                ]
                                                        }) \
            .sort([('last_time_crawl_profile', 1)]) \
            .limit(_num_user)
        return result

    # endregion

    # region Change Identity Status

    def _change_identity_status_to(self,
                                   _users,
                                   _identity_status,
                                   _save_current_time=False):
        if not _users:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _user in _users:
            _record = {'crawl_identity_status': _identity_status}
            if _save_current_time:
                _record['last_time_crawl_identity'] = _current_timestamp
            _updated_records.append([{'_id': _user['_id']},
                                     _record])
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        if service_result:
            return service_result
        return 'success'

    # ********** Change crawl_identity_status of KOLs to Pending **********
    def change_identity_status_to_pending(self,
                                          _users):
        return self._change_identity_status_to(_users=_users,
                                               _identity_status=CrawlStatusEnum.Pending)

    # ********** Change crawl_identity_status of KOLs to Cached **********
    def change_identity_status_to_cached(self,
                                         _users):
        return self._change_identity_status_to(_users=_users,
                                               _identity_status=CrawlStatusEnum.Cached,
                                               _save_current_time=True)

    # ********** Change crawl_identity_status of KOLs to Queuing **********
    def change_identity_status_to_queuing(self,
                                          _users):
        return self._change_identity_status_to(_users=_users,
                                               _identity_status=CrawlStatusEnum.Queuing,
                                               _save_current_time=True)

    # endregion

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
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        if service_result:
            return service_result
        return 'success'

    # ********** Change crawl_profile_status of KOLs to Pending **********
    def change_profile_status_to_pending(self,
                                         _users):
        return self._change_profile_status_to(_users=_users,
                                              _profile_status=CrawlStatusEnum.Pending)

    # ********** Change crawl_profile_status of KOLs to Cached **********
    def change_profile_status_to_cached(self,
                                        _users):
        return self._change_profile_status_to(_users=_users,
                                              _profile_status=CrawlStatusEnum.Cached,
                                              _save_current_time=True)

    # ********** Change crawl_profile_status of KOLs to Queuing **********
    def change_profile_status_to_queuing(self,
                                         _users):
        return self._change_profile_status_to(_users=_users,
                                              _profile_status=CrawlStatusEnum.Queuing,
                                              _save_current_time=True)

    # endregion

    def change_response_server_to_unsend(self, _users):
        """Set signal to resend the information of these users to Web Server. \n
                Set value of num_update in response_server object to 0 to resend data of users to
                Web Server

                Parameters
                ----------
                _users : List[Dict]
                    A list of KOLs

                Returns
                -------
                Json Object
                    Result of updated service
                """

        if not _users:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _user in _users:
            _record = {'response_server.num_update': 0,
                       'response_server.last_time_update': _current_timestamp}
            _updated_records.append([{'_id': _user['_id']},
                                     _record])
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records,
                                                             _upsert=False)

        if service_result:
            return service_result
        return 'success'

    # region Change Analyze Fandemo Status

    def _change_analyze_fandemo_status_to(self,
                                          _kols,
                                          _analyze_fandemo_status,
                                          _save_current_time=False):
        if not _kols:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _kol in _kols:
            _record = {'analyze_fandemo_status': _analyze_fandemo_status}
            if _save_current_time:
                _record['last_time_analyze_fandemo'] = _current_timestamp
            _updated_records.append([{'_id': _kol['_id']},
                                     _record])
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    # ********** Change analyze_fandemo_status of kols to Pending **********
    def change_analyze_fandemo_status_to_pending(self, _kols):
        return self._change_analyze_fandemo_status_to(_kols=_kols,
                                                      _analyze_fandemo_status=DocStatusEnum.Pending)

    # ********** Change analyze_fandemo_status of kols to Cached  **********
    def change_analyze_fandemo_status_to_cached(self, _kols):
        return self._change_analyze_fandemo_status_to(_kols=_kols,
                                                      _analyze_fandemo_status=DocStatusEnum.Cached)

    # ********** Change analyze_fandemo_status of kols to Queuing **********
    def change_analyze_fandemo_status_to_queuing(self, _kols):
        return self._change_analyze_fandemo_status_to(_kols=_kols,
                                                      _analyze_fandemo_status=DocStatusEnum.Queuing)

    # end region

    # region Get Kols to Analyze FanDemo

    # ********** Get KOLs where analyze_fandemo_status is Pending **********
    def get_pending_fandemo_kols(self,
                                 _num_kol=5):
        result = self.kol_dbhandler.get_many_by_filter({'last_time_crawl_profile': {'$exists': True},
                                                        'analyze_fandemo_status': DocStatusEnum.Pending
                                                        }).limit(_num_kol)
        return result

    # ********** Get KOLs where analyze_fandemo_status is Not Exist **********
    def get_not_exist_fandemo_kols(self,
                                   _num_kol=5):
        result = self.kol_dbhandler.get_many_by_filter({'last_time_crawl_profile': {'$exists': True},
                                                        'analyze_fandemo_status': {'$exists': False}
                                                        }).limit(_num_kol)
        return result

    # ********** Get KOLs where analyze_fandemo_status is Analyzed **********
    def get_old_fandemo_kols(self,
                             _num_kol=5,
                             _duration_refresh=43200):
        _curr_timestamp = DateHelper.current_itimestamp()
        _thre_timestamp = _curr_timestamp - _duration_refresh
        result = self.kol_dbhandler.get_many_by_filter({'last_time_crawl_profile': {'$exists': True},
                                                        'analyze_fandemo_status': DocStatusEnum.Analyzed,
                                                        'last_time_analyze_fandemo': {'$lt': _thre_timestamp}
                                                        }).limit(_num_kol)
        return result

    # endregion

    # region Get Kols to Analyze Fakerate

    # ********** Get KOLs where analyze_fakerate_status is Pending **********
    def get_pending_fakerate_kols(self,
                                  _num_kol=5):
        result = self.kol_dbhandler.get_many_by_filter({'last_time_crawl_profile': {'$exists': True},
                                                        'analyze_fakerate_status': DocStatusEnum.Pending
                                                        }).limit(_num_kol)
        return result

    # ********** Get KOLs where analyze_fakerate_status is Not Exist **********
    def get_not_exist_fakerate_kols(self,
                                    _num_kol=5):
        result = self.kol_dbhandler.get_many_by_filter({'last_time_crawl_profile': {'$exists': True},
                                                        'analyze_fakerate_status': {'$exists': False}
                                                        }).limit(_num_kol)
        return result

    # ********** Get KOLs where analyze_fakerate_status is Analyzed **********
    def get_old_fakerate_kols(self,
                              _num_kol=5,
                              _duration_refresh=43200):
        _curr_timestamp = DateHelper.current_itimestamp()
        _thre_timestamp = _curr_timestamp - _duration_refresh
        result = self.kol_dbhandler.get_many_by_filter(_filter={'last_time_crawl_profile': {'$exists': True},
                                                                'analyze_fakerate_status': DocStatusEnum.Analyzed,
                                                                'last_time_analyze_fakerate': {'$lt': _thre_timestamp}
                                                                }).limit(_num_kol)
        return result

    # endregion

    # region Get Kols to Analyze subtopic

    # ********** Priority 1: Get kols where must analyze subtopic **********
    def get_pending_subtopic_kols(self, _num_kol=50):
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'last_time_crawl_post': {'$exists': True},
                'analyze_subtopic_status': DocStatusEnum.Pending},
            _selected_fields=['_id', 'user_id', 'page_id', 'username', 'hiip_user_type', 'country_code']) \
            .limit(_num_kol)
        return result

    # ********** Priority 2: Get kols where does not analyze subtopic **********
    def get_not_exist_subtopic_kols(self, _num_kol=50):
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'last_time_crawl_post': {'$exists': True},
                'analyze_subtopic_status': {'$exists': False}},
            _selected_fields=['_id', 'user_id', 'page_id', 'username', 'hiip_user_type', 'country_code']) \
            .limit(_num_kol)
        return result

    # ********** Priority 3: Get old kols where have old subtopic **********
    def get_old_subtopic_kols(self,
                              _num_kol=50,
                              _duration_refresh=43200):
        _current_timestamp = time.time()
        _last_timestamp = _current_timestamp - _duration_refresh
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'last_time_crawl_post': {'$exists': True},
                'analyze_subtopic_status': DocStatusEnum.Analyzed,
                'last_time_analyze_subtopic': {'$lt': _last_timestamp}},
            _selected_fields=['_id', 'user_id', 'page_id', 'username', 'hiip_user_type', 'country_code']) \
            .sort([('last_time_analyze_subtopic', 1)]) \
            .limit(_num_kol)
        return result

    # endregion

    # region Get Kols to Analyze Interaction

    # ********** Priority 1: Get kols where must analyze interaction **********
    def get_pending_interaction_kols(self, _num_kol=50):
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'last_time_crawl_post': {'$exists': True},
                'analyze_interaction_status': DocStatusEnum.Pending},
            _selected_fields=['_id', 'user_id', 'page_id', 'username', 'hiip_user_type']) \
            .limit(_num_kol)
        return result

    # ********** Priority 2: Get kols where does not analyze interaction **********
    def get_not_exist_interaction_kols(self, _num_kol=50):
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'last_time_crawl_post': {'$exists': True},
                'analyze_interaction_status': {'$exists': False}},
            _selected_fields=['_id', 'user_id', 'page_id', 'username', 'hiip_user_type']) \
            .limit(_num_kol)
        return result

    # ********** Priority 3: Get old kols where have old interaction **********
    def get_old_interaction_kols(self,
                                 _num_kol=50,
                                 _duration_refresh=43200):
        _current_timestamp = time.time()
        _last_timestamp = _current_timestamp - _duration_refresh
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'last_time_crawl_post': {'$exists': True},
                'analyze_interaction_status': DocStatusEnum.Analyzed,
                'last_time_analyze_interaction': {'$lt': _last_timestamp}},
            _selected_fields=['_id', 'user_id', 'page_id', 'username', 'hiip_user_type']) \
            .sort([('last_time_analyze_interaction', 1)]) \
            .limit(_num_kol)
        return result

    # endregion

    # region Get Kols to Analyze Branded Post

    # ********** Priority 1: Get kols where must analyze branded post **********
    def get_pending_branded_post_kols(self, _num_kol=50):
        result = self.kol_dbhandler.get_many_by_filter(_filter={'crawl_post_status': DocStatusEnum.Crawled,
                                                                'analyze_branded_post_status': DocStatusEnum.Pending},
                                                       _selected_fields=['_id',
                                                                         'hiip_user_type', 'fb_user_type',
                                                                         'user_id', 'page_id', 'username']) \
            .limit(_num_kol)
        return result

    # ********** Priority 2: Get kols where does not analyze branded post **********
    def get_not_exist_branded_post_kols(self, _num_kol=50):
        result = self.kol_dbhandler.get_many_by_filter(_filter={'crawl_post_status': DocStatusEnum.Crawled,
                                                                'analyze_branded_post_status': {'$exists': False}},
                                                       _selected_fields=['_id',
                                                                         'hiip_user_type', 'fb_user_type',
                                                                         'user_id', 'page_id', 'username']) \
            .limit(_num_kol)
        return result

    # ********** Priority 3: Get old kols where have old branded post **********
    def get_old_branded_post_kols(self,
                                  _num_kol=50,
                                  _duration_refresh=43200):
        _current_timestamp = DateHelper.current_itimestamp()
        _last_timestamp = _current_timestamp - _duration_refresh
        result = self.kol_dbhandler.aggregate([{'$match': {'crawl_post_status': DocStatusEnum.Crawled,
                                                           'analyze_branded_post_status': DocStatusEnum.Analyzed,
                                                           'last_time_analyze_branded_post': {'$lt': _last_timestamp}}},
                                               {'$sort': {'last_time_analyze_branded_post': 1}},
                                               {'$limit': _num_kol},
                                               {'$project': {
                                                   '_id': 1,
                                                   'hiip_user_type': 1, 'fb_user_type': 1,
                                                   'user_id': 1, 'page_id': 1, 'username': 1
                                               }}])
        return result

    # endregion

    # region Change Analyze Fakerate Status

    def _change_analyze_fakerate_status_to(self,
                                           _kols,
                                           _analyze_fakerate_status,
                                           _save_current_time=False):
        if not _kols:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _kol in _kols:
            _record = {'analyze_fakerate_status': _analyze_fakerate_status}
            if _save_current_time:
                _record['last_time_analyze_fakerate'] = _current_timestamp
            _updated_records.append([{'_id': _kol['_id']},
                                     _record])
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    # ********** Change analyze_fakerate_status of kols to Pending **********
    def change_analyze_fakerate_status_to_pending(self, _kols):
        return self._change_analyze_fakerate_status_to(_kols=_kols,
                                                       _analyze_fakerate_status=DocStatusEnum.Pending)

    # ********** Change analyze_fakerate_status of kols to Cached  **********
    def change_analyze_fakerate_status_to_cached(self, _kols):
        return self._change_analyze_fakerate_status_to(_kols=_kols,
                                                       _analyze_fakerate_status=DocStatusEnum.Cached)

    # ********** Change analyze_fakerate_status of kols to Queuing **********
    def change_analyze_fakerate_status_to_queuing(self, _kols):
        return self._change_analyze_fakerate_status_to(_kols=_kols,
                                                       _analyze_fakerate_status=DocStatusEnum.Queuing)

    # end region

    # region Get Kols to Calculate Topic Post

    # ********** Get KOLs where analyze_topic_post_status is Pending **********
    def get_pending_topic_post_kols(self,
                                    _num_kol=5):
        result = self.kol_dbhandler.get_many_by_filter({'last_time_crawl_profile': {'$exists': True},
                                                        'analyze_topic_post_status': DocStatusEnum.Pending
                                                        }).limit(_num_kol)
        return result

    # ********** Get KOLs where analyze_topic_post_status is Not Exist **********
    def get_not_exist_topic_post_kols(self,
                                      _num_kol=5):
        result = self.kol_dbhandler.get_many_by_filter({'last_time_crawl_profile': {'$exists': True},
                                                        'analyze_topic_post_status': {'$exists': False}
                                                        }).limit(_num_kol)
        return result

    # ********** Get KOLs where analyze_topic_post_status is Analyzed **********
    def get_old_topic_post_kols(self,
                                _num_kol=5,
                                _duration_refresh=43200):
        _curr_timestamp = DateHelper.current_itimestamp()
        _thre_timestamp = _curr_timestamp - _duration_refresh
        result = self.kol_dbhandler.get_many_by_filter({'last_time_crawl_profile': {'$exists': True},
                                                        'analyze_topic_post_status': DocStatusEnum.Analyzed,
                                                        'last_time_analyze_topic_post': {'$lt': _thre_timestamp}
                                                        }).limit(_num_kol)
        return result

    # endregion

    # region Change Interaction Status

    def _change_interaction_status_to(self,
                                      _kols,
                                      _interaction_status,
                                      _save_current_time=False):
        if not _kols:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _kol in _kols:
            _record = {'analyze_interaction_status': _interaction_status}
            if _save_current_time:
                _record['last_time_analyze_interaction'] = _current_timestamp
            _updated_records.append([{'_id': _kol['_id']},
                                     _record])
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    # ********** Change analyze_interaction_status of kols to Pending **********
    def change_interaction_status_to_pending(self, _kols):
        return self._change_interaction_status_to(_kols=_kols,
                                                  _interaction_status=DocStatusEnum.Pending)

    # ********** Change analyze_interaction_status of kols to Cached **********
    def change_interaction_status_to_cached(self,
                                            _kols):
        return self._change_interaction_status_to(_kols=_kols,
                                                  _interaction_status=DocStatusEnum.Cached)

    # ********** Change analyze_interaction_status of kols to Queuing **********
    def change_interaction_status_to_queuing(self, _kols):
        return self._change_interaction_status_to(_kols=_kols,
                                                  _interaction_status=DocStatusEnum.Queuing,
                                                  _save_current_time=True)

    # endregion

    # region Change subtopic Status

    def _change_subtopic_status_to(self,
                                   _kols,
                                   _subtopic_status,
                                   _save_current_time=False):
        if not _kols:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _kol in _kols:
            _record = {'analyze_subtopic_status': _subtopic_status}
            if _save_current_time:
                _record['last_time_analyze_subtopic'] = _current_timestamp
            _updated_records.append([{'_id': _kol['_id']},
                                     _record])
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    # ********** Change analyze_subtopic_status of kols to Cached **********
    def change_subtopic_status_to_cached(self,
                                         _kols):
        return self._change_subtopic_status_to(_kols=_kols,
                                               _subtopic_status=DocStatusEnum.Cached)

    # ********** Change analyze_subtopic_status of kols to Queuing **********
    def change_subtopic_status_to_queuing(self, _kols):
        return self._change_subtopic_status_to(_kols=_kols,
                                               _subtopic_status=DocStatusEnum.Queuing,
                                               _save_current_time=True)

    # endregion

    # region Change Branded Post Status

    def _change_branded_post_status_to(self,
                                       _kols,
                                       _branded_post_status,
                                       _save_current_time=False):
        if not _kols:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _kol in _kols:
            _record = {'analyze_branded_post_status': _branded_post_status}
            if _save_current_time:
                _record['last_time_analyze_branded_post'] = _current_timestamp
            _updated_records.append([{'_id': _kol['_id']},
                                     _record])
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    # ********** Change analyze_branded_post_status of kols to Cached **********
    def change_branded_post_status_to_cached(self,
                                             _kols):
        return self._change_branded_post_status_to(_kols=_kols,
                                                   _branded_post_status=DocStatusEnum.Cached)

    # ********** Change analyze_branded_post_status of kols to Queuing **********
    def change_branded_post_status_to_queuing(self, _kols):
        return self._change_branded_post_status_to(_kols=_kols,
                                                   _branded_post_status=DocStatusEnum.Queuing,
                                                   _save_current_time=True)

    # endregion

    # region Change Topic Post Status

    def _change_topic_post_status_to(self,
                                     _kols,
                                     _topic_post_status,
                                     _save_current_time=False):
        if not _kols:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _kol in _kols:
            _record = {'analyze_topic_post_status': _topic_post_status}
            if _save_current_time:
                _record['last_time_analyze_topic_post'] = _current_timestamp
            _updated_records.append([{'_id': _kol['_id']},
                                     _record])
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    # ********** Change analyze_interaction_status of kols to Cached **********
    def change_topic_post_status_to_cached(self, _kols):
        return self._change_topic_post_status_to(_kols=_kols,
                                                 _topic_post_status=DocStatusEnum.Cached)

    # ********** Change analyze_interaction_status of kols to Queuing **********
    def change_topic_post_status_to_queuing(self, _kols):
        return self._change_topic_post_status_to(_kols=_kols,
                                                 _topic_post_status=DocStatusEnum.Queuing)

    # endregion

    # region Get Kols to Crawl Their post

    # ********** Get kols where crawl_post_status is Pending **********
    def get_pending_post_status_kols(self,
                                     _num_kol=20):
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'last_time_crawl_profile': {'$exists': True},
                'crawl_post_status': DocStatusEnum.Pending},
            _selected_fields=[
                '_id',
                'hiip_user_type', 'fb_user_type', 'fb_permission',
                'user_id', 'page_id', 'username', 'app_id']) \
            .limit(_num_kol)
        return result

    def get_kols_influence_type_sort(self, _filter, _sort, _num_kol=20):
        result = self.kol_dbhandler \
            .get_many_by_filter_and_sort(
            _filter=_filter,
            _sort=_sort,
            _selected_fields=[
                '_id',
                'hiip_user_type', 'fb_user_type', 'fb_permission',
                'user_id', 'page_id', 'username', 'app_id']) \
            .limit(_num_kol)
        return result

    def get_pending_post_performance_status_kols(self,
                                                 _num_kol=20):
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'analyze_post_performance_status': DocStatusEnum.Pending},
            _selected_fields=['_id', 'user_id', 'page_id']) \
            .limit(_num_kol)
        return result

    def get_pending_fan_age_gender_status_kols(self, _num_kol=20):
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'analyze_fan_age_gender_status': DocStatusEnum.Pending},
            _selected_fields=['_id', 'user_id', 'page_id']) \
            .limit(_num_kol)
        return result

    # ********** Get kols where crawl_post_status is Not Exist **********
    def get_not_exist_post_status_kols(self,
                                       _num_kol=20):
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'last_time_crawl_profile': {'$exists': True},
                'crawl_post_status': {'$exists': False}},
            _selected_fields=[
                '_id',
                'hiip_user_type', 'fb_user_type', 'fb_permission',
                'user_id', 'page_id', 'username', 'app_id']) \
            .limit(_num_kol)
        return result

    def get_not_exist_post_performance_status_kols(self,
                                                   _num_kol=20):
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'last_time_crawl_post': {'$exists': True},
                'analyze_post_performance_status': {'$exists': False}},
            _selected_fields=['_id', 'user_id', 'page_id']) \
            .limit(_num_kol)
        return result

    def get_not_exist_fan_age_gender_status_kols(self,
                                                 _num_kol=20):
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'last_time_crawl_post': {'$exists': True},
                'analyze_fan_age_gender_status': {'$exists': False}},
            _selected_fields=['_id', 'user_id', 'page_id']) \
            .limit(_num_kol)
        return result

    # ********** Get kols where crawl_post_status is Crawled **********
    def get_crawled_post_status_kols(self,
                                     _num_kol=20,
                                     _duration_refresh=43200):
        _current_timestamp = time.time()
        _last_timestamp = _current_timestamp - _duration_refresh
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'last_time_crawl_profile': {'$exists': True},
                'crawl_post_status': DocStatusEnum.Crawled,
                'last_time_crawl_post': {'$lt': _last_timestamp}},
            _selected_fields=[
                '_id',
                'hiip_user_type', 'fb_user_type', 'fb_permission',
                'user_id', 'page_id', 'username', 'app_id']) \
            .sort([('last_time_crawl_post', 1)]) \
            .limit(_num_kol)
        return result

    def get_analyzed_post_performance_status_kols(self,
                                                  _num_kol=20,
                                                  _duration_refresh=43200):
        _current_timestamp = time.time()
        _last_timestamp = _current_timestamp - _duration_refresh
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'last_time_analyze_post_performance': {'$lt': _last_timestamp}},
            _selected_fields=['_id', 'user_id', 'page_id']) \
            .sort([('last_time_analyze_post_performance', 1)]) \
            .limit(_num_kol)
        return result

    def get_analyzed_fan_age_gender_status_kols(self,
                                                _num_kol=20,
                                                _duration_refresh=43200):
        _current_timestamp = time.time()
        _last_timestamp = _current_timestamp - _duration_refresh
        result = self.kol_dbhandler \
            .get_many_by_filter(
            _filter={
                'last_time_analyze_fan_age_gender': {'$lt': _last_timestamp}},
            _selected_fields=['_id', 'user_id', 'page_id']) \
            .sort([('last_time_analyze_fan_age_gender', 1)]) \
            .limit(_num_kol)
        return result

    # endregion

    # region Change Post Status
    def _change_fb_permission_user_post(self,
                                        _kols,
                                        _granted_status):
        """
        Update fb_permission for user_posts
        """
        if not _kols:
            return 'success'
        _updated_records = []
        for _kol in _kols:
            # Get kols permission
            _fb_permission = self.kol_dbhandler.get_one_by_id(_kol['_id'], ['fb_permission'])
            fb_permission = _fb_permission['fb_permission']

            for item in fb_permission:
                if item['permission'] == 'user_posts':
                    item['status'] = _granted_status
            _record = {'fb_permission': fb_permission}
            # Update permission
            _updated_records.append([{'_id': _kol['_id']},
                                     _record])

        print(_updated_records)
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    def _change_post_status_to(self,
                               _kols,
                               _post_status,
                               _save_current_time=False):
        if not _kols:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _kol in _kols:
            _record = {'crawl_post_status': _post_status}
            if _save_current_time:
                _record['last_time_crawl_post'] = _current_timestamp
            _updated_records.append([{'_id': _kol['_id']},
                                     _record])
        print(_updated_records)
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    def _change_analyze_interaction_status_to(self,
                                              _kols,
                                              _profile_status,
                                              _save_current_time=False):
        if not _kols:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _kol in _kols:
            _record = {'analyze_interaction_status': _profile_status}
            _updated_records.append([{'_id': _kol['_id']},
                                     _record])
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)
        print(_updated_records)
        return service_result

    def _change_post_performance_status_to(self,
                                           _kols,
                                           _post_performance_status,
                                           _save_current_time=False):
        if not _kols:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _kol in _kols:
            _record = {'analyze_post_performance_status': _post_performance_status}
            if _save_current_time:
                _record['last_time_analyze_post_performance'] = _current_timestamp
            _updated_records.append([{'_id': _kol['_id']},
                                     _record])
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    # ********** Change crawl_profile_status of KOLs to Crawled **********
    def change_analyze_interaction_status_to_pending(self,
                                                     _users):
        return self._change_analyze_interaction_status_to(_kols=_users,
                                                          _profile_status=CrawlStatusEnum.Pending)

    # change Granted
    def change_fb_permission_user_post_to_not_granted(self,
                                                      _kols):
        return self._change_fb_permission_user_post(_kols, 'not_granted')

    # ********** Change crawl_post_status of kols to Pending **********
    def change_post_status_to_pending(self,
                                      _kols):
        return self._change_post_status_to(_kols=_kols,
                                           _post_status=DocStatusEnum.Pending)

        # ********** Change crawl_post_status of kols to Error **********

    def change_post_status_to_error(self,
                                    _kols):
        return self._change_post_status_to(_kols=_kols,
                                           _post_status=DocStatusEnum.Error,
                                           _save_current_time=True)

    # ********** Change crawl_post_status of kols to Cached **********
    def change_post_status_to_cached(self,
                                     _kols):
        return self._change_post_status_to(_kols=_kols,
                                           _post_status=DocStatusEnum.Cached)

    # ********** Change crawl_post_status of kols to Queuing **********
    def change_post_status_to_queuing(self,
                                      _kols):
        return self._change_post_status_to(_kols=_kols,
                                           _post_status=DocStatusEnum.Queuing)

    # ********** Change crawl_post_status of kols to Crawling **********
    def change_post_status_to_crawling(self,
                                       _kols):
        return self._change_post_status_to(_kols=_kols,
                                           _post_status=DocStatusEnum.Crawling)

    # ********** Change crawl_post_status of kols to Crawler **********
    def change_post_status_to_crawled(self,
                                      _kols):
        return self._change_post_status_to(_kols=_kols,
                                           _post_status=DocStatusEnum.Crawled,
                                           _save_current_time=True)

    def change_post_status_to_failed(self,
                                     _kols):
        return self._change_post_status_to(_kols=_kols,
                                           _post_status=DocStatusEnum.Failed,
                                           _save_current_time=True)

    def change_post_status_to_expired(self,
                                      _kols):
        return self._change_post_status_to(_kols=_kols,
                                           _post_status=DocStatusEnum.Expired)

    def change_post_performance_status_to_cached(self, _kols):
        return self._change_post_performance_status_to(_kols=_kols,
                                                       _post_performance_status=DocStatusEnum.Cached)

    def change_post_performance_status_to_queuing(self, _kols):
        return self._change_post_performance_status_to(_kols=_kols,
                                                       _post_performance_status=DocStatusEnum.Queuing)

    def change_fan_age_gender_status_to_cached(self, _kols):
        return self._change_fan_age_gender_status_to(_kols=_kols,
                                                     _fan_age_gender_status=DocStatusEnum.Cached)

    def change_fan_age_gender_status_to_queuing(self, _kols):
        return self._change_fan_age_gender_status_to(_kols=_kols,
                                                     _fan_age_gender_status=DocStatusEnum.Queuing)

    def _change_fan_age_gender_status_to(self,
                                         _kols,
                                         _fan_age_gender_status,
                                         _save_current_time=False):
        if not _kols:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _kol in _kols:
            _record = {'analyze_fan_age_gender_status': _fan_age_gender_status}
            if _save_current_time:
                _record['last_time_analyze_fan_age_gender'] = _current_timestamp
            _updated_records.append([{'_id': _kol['_id']},
                                     _record])
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    # end region

    # region Get Kols to Crawl Their Reactions

    # ********** Get KOLs where crawl_reaction_status is Pending **********
    def get_pending_reaction_status_kols(self,
                                         _num_kol=10):
        result = self.kol_dbhandler \
            .get_many_by_filter(_filter={'last_time_analyze_interaction': {'$exists': True},
                                         'crawl_reaction_status': DocStatusEnum.Pending},
                                _selected_fields=['_id', 'user_id', 'page_id', 'username',
                                                  'last_time_crawl_reaction',
                                                  'hiip_user_type', 'fb_user_type']) \
            .limit(_num_kol)
        return result

    # ********** Get KOLs where crawl_reaction_status is not exist **********
    def get_not_exist_reaction_status_kols(self,
                                           _num_kol=10):
        result = self.kol_dbhandler \
            .get_many_by_filter(_filter={'last_time_analyze_interaction': {'$exists': True},
                                         'crawl_reaction_status': {'$exists': False}},
                                _selected_fields=['_id', 'user_id', 'username',
                                                  'last_time_crawl_reaction',
                                                  'hiip_user_type', 'fb_user_type']) \
            .limit(_num_kol)
        return result

    # ********** Get KOLs where crawl_reaction_status is Unselected **********
    def get_unselected_reaction_status_kols(self,
                                            _num_kol=10,
                                            _duration_refresh=43200):
        _curr_timestamp = DateHelper.current_itimestamp()
        _thre_timestamp = _curr_timestamp - _duration_refresh
        result = self.kol_dbhandler.aggregate([{'$match': {'last_time_analyze_interaction': {'$exists': True},
                                                           'crawl_reaction_status': DocStatusEnum.Unselected,
                                                           'last_time_crawl_reaction': {'$lt': _thre_timestamp}}},
                                               {'$sort': {'crawl_reaction_score': 1}},
                                               {'$limit': _num_kol},
                                               {'$project': {
                                                   '_id': 1,
                                                   'user_id': 1,
                                                   'username': 1,
                                                   'last_time_crawl_reaction': 1,
                                                   'hiip_user_type': 1,
                                                   'fb_user_type': 1
                                               }
                                               }])
        return result

    # endregion

    # region Change reaction Status

    def _change_reaction_status_to(self,
                                   _kols,
                                   _reaction_status,
                                   _save_current_time=False):
        if not _kols:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _kol in _kols:
            _record = {'crawl_reaction_status': _reaction_status}
            if _save_current_time:
                _record['last_time_crawl_reaction'] = _current_timestamp
            _updated_records.append([{'_id': _kol['_id']},
                                     _record])
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    # ********** Change crawl_reaction_status of posts to Pending **********
    def change_reaction_status_to_pending(self,
                                          _kols):
        return self._change_reaction_status_to(_kols=_kols,
                                               _reaction_status=DocStatusEnum.Pending)

    # ********** Change crawl_reaction_status of posts to Cached **********
    def change_reaction_status_to_cached(self,
                                         _kols):
        return self._change_reaction_status_to(_kols=_kols,
                                               _reaction_status=DocStatusEnum.Cached)

    # ********** Change crawl_reaction_status of posts to Queuing **********
    def change_reaction_status_to_queuing(self,
                                          _kols):
        return self._change_reaction_status_to(_kols=_kols,
                                               _reaction_status=DocStatusEnum.Queuing)

    # endregion

    # region Change Check Data Status

    def _change_data_status_to(self,
                               _kols,
                               _data_status,
                               _save_current_time=False):
        if not _kols:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _kol in _kols:
            _record = {'check_data_status': _data_status}
            if _save_current_time:
                _record['last_time_check_data'] = _current_timestamp
            _updated_records.append([{'_id': _kol['_id']},
                                     _record])
        service_result = self.kol_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    # ********** Change check_data_status of kols to Cached **********
    def change_data_status_to_cached(self,
                                     _kols):
        return self._change_data_status_to(_kols=_kols,
                                           _data_status=DocStatusEnum.Cached)

    # ********** Change check_data_status of kols to Analyzing **********
    def change_data_status_to_analyzing(self, _kols):
        return self._change_data_status_to(_kols=_kols,
                                           _data_status=DocStatusEnum.Analyzing)

    # ********** Change check_data_status of kols to Analyzed **********
    def change_data_status_to_analyzed(self, _kols):
        return self._change_data_status_to(_kols=_kols,
                                           _data_status=DocStatusEnum.Analyzed,
                                           _save_current_time=True)

    # endregion

    # region Get Kols to Check Data

    def get_urgent_check_data_kols(self,
                                   _num_kol=2):
        result = self.kol_dbhandler.get_many_by_filter(_filter={'check_data_status': DocStatusEnum.Pending},
                                                       _selected_fields=['user_id']).limit(_num_kol)
        return result

    def get_new_check_data_kols(self,
                                _num_kol=5):
        result = self.kol_dbhandler.get_many_by_filter(_filter={'check_data_status': {'$exists': False}},
                                                       _selected_fields=['user_id']).limit(_num_kol)
        return result

    def get_normal_check_data_kols(self,
                                   _average_reaction_from=None,
                                   _average_reaction_to=None,
                                   _duration_refresh=3600 * 24 * 7,  # 7 days
                                   _num_kol=3):
        _like_condition = {}
        if _average_reaction_from:
            _like_condition['$gte'] = _average_reaction_from
        if _average_reaction_to:
            _like_condition['$lt'] = _average_reaction_to
        _current_timestamp = DateHelper.current_itimestamp()
        _threshold_timestamp = _current_timestamp - _duration_refresh
        result = self.kol_dbhandler.aggregate([{'$match': {'check_data_status': DocStatusEnum.Analyzed,
                                                           'average_reaction': _like_condition,
                                                           'last_time_check_data': {'$lt': _threshold_timestamp}
                                                           }},
                                               {'$sort': {'last_time_check_data': 1}},
                                               {'$limit': _num_kol},
                                               {'$project': {
                                                   '_id': 1,
                                                   'user_id': 1,
                                                   'average_reaction': 1,
                                                   'priority': 1
                                               }}])
        return result

    def get_hot_normal_check_data_kols(self,
                                       _average_reaction_from=None,
                                       _average_reaction_to=None,
                                       _reaction_ratio=0.2,
                                       _num_kol=3):
        _like_condition = {}
        if _average_reaction_from:
            _like_condition['$gte'] = _average_reaction_from
        if _average_reaction_to:
            _like_condition['$lt'] = _average_reaction_to
        result = self.kol_dbhandler.aggregate([{'$match': {'check_data_status': DocStatusEnum.Analyzed,
                                                           'average_reaction': _like_condition,
                                                           'crawled_like_ratio': {'$lt': _reaction_ratio}
                                                           }},
                                               {'$sort': {'last_time_check_data': 1}},
                                               {'$limit': _num_kol},
                                               {'$project': {
                                                   '_id': 1,
                                                   'user_id': 1,
                                                   'average_reaction': 1,
                                                   'priority': 1
                                               }}])
        return result

    # endregion

    # region Update Kol Check Data

    def update_check_data_kols(self,
                               _kols):
        _kol_objs = []
        for _kol in _kols:
            _kol_obj = {}
            DictHelper.transfer_fields(_from=_kol,
                                       _to=_kol_obj,
                                       _fields=['_id'])
            _kol_objs.append([{'_id': _kol_obj['_id']},
                              _kol_obj])
        result = self.kol_dbhandler.update_many_pair(_updated_records=_kol_objs)
        return result

    # endregion

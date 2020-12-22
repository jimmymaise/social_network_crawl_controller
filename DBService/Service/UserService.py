# Import libs
import time  # Time lib
import uuid

# Import Models
from DBService.Models.Media import MediaModel
from DBService.Models.Page import PageModel
from DBService.Models.CrawlStatusEnum import CrawlStatusEnum

# Import DBHandler
from DBService.DBHandler.UserDBHandler import UserDBHandler
from DBService.DBHandler.MediaDBHandler import MediaDBHandler
from DBService.DBHandler.PageDBHandler import PageDBHandler
from DBService.DBHandler.PostDBHandler import PostDBHandler
from DBService.DBHandler.NormalUserDBHandler import NormalUserDBHandler
from DBService.DBHandler.UserFollowUserDBHandler import UserFollowUserDBHandler
from DBService.DBHandler.KOLDBHandler import KOLDBHandler

# Import Utils
from SuperUtils.HashHelper import HashHelper
from SuperUtils import DictHelper, AwsS3Helper


# pylint: disable=R0904
class UserService(object):
    # ********** Constructor **********
    def __init__(self):
        self.user_dbhandler = UserDBHandler()
        self.media_dbhandler = MediaDBHandler()
        self.page_dbhandler = PageDBHandler()
        self.post_dbhandler = PostDBHandler()
        self.kol_dbhandler = KOLDBHandler()
        self.normaluser_dbhandler = NormalUserDBHandler()
        self.userfollowuser_dbhandler = UserFollowUserDBHandler()

    # ========== Update profile info of Users ===============
    def _extract_profile_data(self,
                              _user_infos):
        # ===== Extract Media | Education | Work | Location =====
        media_objs = []
        page_objs = []
        for _user_info in _user_infos:
            _user = _user_info['body']
            if _user_info['code'] == 200:
                # --- Set avatar ---
                if 'avatar' in _user and _user['avatar']:
                    _link = _user['avatar']
                    _id = HashHelper.hash(_link + str(uuid.uuid4()))
                    _s3_link = AwsS3Helper.upload_image_to_s3_and_get_link(_image_url=_link,
                                                                           _id=_id)
                    _media_obj = MediaModel.create_with(_link=_link, _s3_link=_s3_link)

                    media_objs.append([{'_id': _media_obj['_id']},
                                       _media_obj])

                    # --- Set reference avatar media_id
                    _user['avatar'] = _media_obj['_id']

                # --- Set cover ---
                if 'cover' in _user and _user['cover']:
                    _link = _user['cover']
                    _id = HashHelper.hash(_link + str(uuid.uuid4()))
                    _s3_link = AwsS3Helper.upload_image_to_s3_and_get_link(_image_url=_link,
                                                                           _id=_id)
                    _media_obj = MediaModel.create_with(_link=_link, _s3_link=_s3_link)
                    media_objs.append([{'_id': _media_obj['_id']},
                                       _media_obj])

                    # --- Set reference cover media_id
                    _user['cover'] = _media_obj['_id']

                # --- Set education ---
                if 'education' in _user:
                    _updated_user_edus = []
                    _user_edus = _user['education']
                    for _user_edu in _user_edus:
                        _edu_obj = PageModel.create_with(_link=_user_edu['link'])
                        _updated_user_edus.append({'text': _user_edu['text'],
                                                   'page_id': _edu_obj['_id']})
                        page_objs.append([{'_id': _edu_obj['_id']},
                                          _edu_obj])

                    # --- Set reference education media_id
                    _user['education'] = _updated_user_edus

                # --- Set work ---
                if 'work' in _user:
                    _updated_user_works = []
                    _user_works = _user['work']
                    for _user_work in _user_works:
                        _work_obj = PageModel.create_with(_link=_user_work['link'])
                        _updated_user_works.append({'text': _user_work['text'],
                                                    'page_id': _work_obj['_id']})
                        page_objs.append([{'_id': _work_obj['_id']},
                                          _work_obj])

                    # --- Set reference education media_id
                    _user['work'] = _updated_user_works

                # --- Set location ---
                if 'location' in _user:
                    _updated_user_locations = []
                    _user_locations = _user['location']
                    for _user_location in _user_locations:
                        _location_obj = PageModel.create_with(_link=_user_location['link'])
                        _updated_user_locations.append({'text': _user_location['text'],
                                                        'page_id': _location_obj['_id']})
                        page_objs.append([{'_id': _location_obj['_id']},
                                          _location_obj])

                    # --- Set reference education media_id
                    _user['location'] = _updated_user_locations

                # --- Set interest ---
                if 'interest' in _user:
                    _updated_user_interests = []
                    _user_interests = _user['interest']
                    for _user_interest in _user_interests:
                        _interest_obj = PageModel.create_with(_link=_user_interest['link'])
                        _updated_user_interests.append({'text': _user_interest['text'],
                                                        'page_id': _interest_obj['_id']})
                        page_objs.append([{'_id': _interest_obj['_id']},
                                          _interest_obj])

                    # --- Set reference education media_id
                    _user['interest'] = _updated_user_interests

                # --- Update to body ---
                _user_info['body'] = _user

        # ===== Extract profile =====
        user_objs = []
        for _user_info in _user_infos:
            _user = _user_info['body']
            if _user_info['code'] == 200:
                _user_obj = {}
                DictHelper.transfer_fields(_user, _user_obj, ['app_id', 'avatar', 'cover', 'full_name', 'intro',
                                                              'nick_name', 'num_follower', 'page_url', 'user_id',
                                                              'username',
                                                              'unknown', 'location', 'education', 'interest', 'work',
                                                              'gender', 'birthday', 'num_photo', 'about'])
                _user_obj['_id'] = _user_obj.pop('user_id', None)  # Remove user_id and transfer user_id to _id
                if self.user_dbhandler.get_one_by_filter({'_id': _user_obj['_id']}, _selected_fields='username'):
                    _user_obj.pop('username', None)
                user_objs.append([{'_id': _user_obj['_id']},
                                  _user_obj])
        return user_objs, media_objs, page_objs

    # ********** Update / Insert Profile Info of Users **********
    def update_profile_info_users(self,
                                  _user_infos):
        # ===== Insert into database =====
        _user_objs, \
        _media_objs, \
        _page_objs = self._extract_profile_data(_user_infos)

        # === Insert media ===
        self.media_dbhandler.update_many_pair(_updated_records=_media_objs,
                                              _upsert=True)

        # === Insert page ===
        self.page_dbhandler.update_many_pair(_updated_records=_page_objs,
                                             _upsert=True)

        # === Insert users ===
        self.user_dbhandler.update_many_pair(_updated_records=_user_objs,
                                             _upsert=True)

        # ===== Return value =====
        return 'success'

    # region Get Users

    # ********** Get user(s) by user_id **********
    def get_user_by_user_id(self,
                            _user_id,
                            _selected_fields=None):
        result = self.user_dbhandler.get_one_by_user_id(_user_id=_user_id,
                                                        _selected_fields=_selected_fields)
        return result

    def get_user_by_app_id(self,
                           _app_id,
                           _selected_fields=None):
        result = self.user_dbhandler.get_one_by_app_id(_app_id=_app_id,
                                                       _selected_fields=_selected_fields)
        return result

    # endregion

    def update_follower_from_comment_info(self,
                                          _post_infos):
        # ===== Update follower relationship table =====
        _followers_objs = self._extract_follower_data_from_post(_post_infos=_post_infos)
        self.userfollowuser_dbhandler.update_many_pair(_updated_records=_followers_objs,
                                                       _upsert=True)

        # ===== Update new users =====
        _newuser_objs = self._extract_newuser_data_from_post(_post_infos=_post_infos)
        if _newuser_objs:
            # --- Parse info ---
            self.normaluser_dbhandler.find_or_create_many_pair(_updated_records=_newuser_objs,
                                                               _upsert=True)

        # ===== Update users info ====
        _user_objs = self._extract_user_data_from_post(_post_infos=_post_infos)
        if _user_objs:
            self.user_dbhandler.update_many_pair(_updated_records=_user_objs,
                                                 _upsert=True)

        # ===== Return value =====
        return 'success'

    def _extract_follower_data_from_post(self,
                                         _post_infos):
        follower_objs = []
        for _post_info in _post_infos:
            _post = _post_info['body']
            if _post_info['code'] == 200:
                _crawled_comments = _post['crawled_comments']
                for _crawled_comment in _crawled_comments:
                    if 'user_id' in _post:
                        _code = str(_post['user_id']) + '|' + str(_crawled_comment['user_id'])
                        _follower_obj = {'_id': HashHelper.hash(_code),
                                         'user_id': _post['user_id'],
                                         'follower_id': _crawled_comment['user_id']}
                    else:
                        _code = str(_post['page_id']) + '|' + str(_crawled_comment['user_id'])
                        _follower_obj = {'_id': HashHelper.hash(_code),
                                         'page_id': _post['page_id'],
                                         'follower_id': _crawled_comment['user_id']}

                    follower_objs.append([{'_id': _follower_obj['_id']},
                                          _follower_obj])
        return follower_objs

    def _extract_newuser_data_from_post(self,
                                        _post_infos):
        _comment_user_objs = []
        for _post_info in _post_infos:
            _post = _post_info['body']
            if _post_info['code'] == 200:
                _crawled_comments = _post['crawled_comments']
                for _crawled_comment in _crawled_comments:
                    _crawl_profile_status = 'Pending'
                    _new_user_obj = {'_id': HashHelper.hash(str(_crawled_comment['user_id'])),
                                     'user_id': _crawled_comment['user_id'],
                                     'username': _crawled_comment['username'],
                                     'crawl_profile_status': _crawl_profile_status}
                    _comment_user_objs.append([{'_id': _new_user_obj['_id']},
                                               _new_user_obj])

        _comment_user_ids = [_comment_user_obj[1]['user_id']
                             for _comment_user_obj in _comment_user_objs]
        _found_user_objs = list(self.kol_dbhandler.get_many_pairs_by_user_id(_user_ids=_comment_user_ids))
        _found_user_ids = [_found_user_obj['user_id']
                           for _found_user_obj in _found_user_objs]
        _new_user_ids = set(_comment_user_ids) - set(_found_user_ids)
        new_user_objs = []
        for _comment_user_obj in _comment_user_objs:
            _user_id = _comment_user_obj[1]['user_id']
            if _user_id in _new_user_ids:
                new_user_objs.append(_comment_user_obj)

        return new_user_objs

    def _extract_user_data_from_post(self,
                                     _post_infos):
        user_objs = []
        for _post_info in _post_infos:
            _post = _post_info['body']
            if _post_info['code'] == 200:
                _crawled_comments = _post['crawled_comments']
                for _crawled_comment in _crawled_comments:
                    _user_obj = {}
                    _user_obj['_id'] = _crawled_comment['user_id']

                    # --- Set username ---
                    _username = DictHelper.get_field(_dict=_crawled_comment, _field_name='username', _otherwise='')
                    _user_obj['username'] = _username

                    # --- Set full_name ---
                    _full_name = DictHelper.get_field(_dict=_crawled_comment, _field_name='full_name', _otherwise='')
                    _user_obj['full_name'] = _full_name

                    # --- Set gender ---
                    _gender = DictHelper.get_field(_dict=_crawled_comment, _field_name='gender', _otherwise=None)
                    if _gender:
                        _user_obj['gender'] = _gender

                    _user_obj = DictHelper.expand_dict(_obj=_user_obj)

                    user_objs.append([{'_id': _user_obj['_id']},
                                      _user_obj])
        return user_objs

    # region Change Post Status

    def _change_post_status_to(self,
                               _users,
                               _post_status,
                               _save_current_time=False):
        if not _users:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _user in _users:
            _record = {'crawl_post_status': _post_status}
            if _save_current_time:
                _record['last_time_crawl_post'] = _current_timestamp
            _updated_records.append([{'_id': _user['_id']},
                                     _record])
        service_result = self.user_dbhandler.update_many_pair(_updated_records=_updated_records)

        if service_result:
            return service_result
        return 'success'

    # ********** Change crawl_post_status of users to Crawling **********
    def change_post_status_to_crawling(self,
                                       _users):
        return self._change_post_status_to(_users=_users,
                                           _post_status=CrawlStatusEnum.Crawling)

    # ********** Change crawl_post_status of users to Crawled **********
    def change_post_status_to_crawled(self,
                                      _users):
        return self._change_post_status_to(_users=_users,
                                           _post_status=CrawlStatusEnum.Crawled,
                                           _save_current_time=True)

    # endregion

    # region Change Reaction Status

    def _change_reaction_status_to(self,
                                   _users,
                                   _reaction_status,
                                   _save_current_time=False):
        if not _users:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _user in _users:
            _record = {'crawl_reaction_status': _reaction_status}
            if _save_current_time:
                _record['last_time_crawl_reaction'] = _current_timestamp
            _updated_records.append([{'_id': _user['_id']},
                                     _record])
        service_result = self.user_dbhandler.update_many_pair(_updated_records=_updated_records)

        if service_result:
            return service_result
        return 'success'

    # ********** Change crawl_reaction_status of users to Crawling **********
    def change_reaction_status_to_crawling(self,
                                           _users):
        return self._change_reaction_status_to(_users=_users,
                                               _reaction_status=CrawlStatusEnum.Crawling)

    # ********** Change crawl_reaction_status of users to Unselected **********
    def change_reaction_status_to_unselected(self,
                                             _users):
        return self._change_reaction_status_to(_users=_users,
                                               _reaction_status=CrawlStatusEnum.Unselected,
                                               _save_current_time=True)

    def get_user_by_username(self,
                             _username,
                             _selected_fields=None):
        found_user = self.user_dbhandler.get_one_by_username(_username=_username,
                                                             _selected_fields=_selected_fields)
        return found_user

    # endregion

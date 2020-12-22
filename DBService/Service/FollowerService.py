# pylint: skip-file
# Import DBHandler
import uuid
from DBService.DBHandler.UserFollowUserDBHandler import UserFollowUserDBHandler
from DBService.DBHandler.MediaDBHandler import MediaDBHandler
from DBService.DBHandler.NormalUserDBHandler import NormalUserDBHandler
from DBService.DBHandler.UserDBHandler import UserDBHandler

# Import Models
from DBService.Models.Media import MediaModel

# Import Utils
from SuperUtils import DictHelper, AwsS3Helper
from SuperUtils.HashHelper import HashHelper


class FollowerService(object):
    # ********** Constructor **********
    def __init__(self):
        self.userfollowuser_dbhandler = UserFollowUserDBHandler()
        self.user_dbhandler = UserDBHandler()
        self.media_dbhandler = MediaDBHandler()
        self.normaluser_dbhandler = NormalUserDBHandler()

    # region Update Followers from Reaction

    def update_follower_from_reac_info_users(self,
                                             _user_infos):
        # ===== Update follower =====
        _followers_objs = self._extract_follower_data_from_reac(_user_infos=_user_infos)
        self.userfollowuser_dbhandler.update_many_pair(_updated_records=_followers_objs,
                                                       _upsert=True)

        # ===== Update new users =====
        _normal_user_objs, \
        _user_objs, \
        _media_objs = self._extract_newuser_data_from_reac(_user_infos=_user_infos)
        if _normal_user_objs:
            # --- Parse info ---
            self.normaluser_dbhandler.find_or_create_many_pair(_updated_records=_normal_user_objs,
                                                               _upsert=True)
            self.user_dbhandler.update_many_pair(_updated_records=_user_objs,
                                                 _upsert=True)
            self.media_dbhandler.update_many_pair(_updated_records=_media_objs,
                                                  _upsert=True)
        # ===== Return value =====
        return 'success'

    def _extract_follower_data_from_reac(self,
                                         _user_infos):
        follower_objs = []
        for _user_info in _user_infos:
            _user = _user_info['body']
            if _user_info['code'] == 200:
                _user_profile = DictHelper.get_field(_dict=_user,
                                                     _field_name='profile',
                                                     _otherwise=None)
                if _user_profile:
                    _latest_posts = DictHelper.get_field(_dict=_user_profile,
                                                         _field_name='latest_posts',
                                                         _otherwise=[])
                    _fb_user_type = _user['fb_user_type']
                    for _post in _latest_posts:
                        if _post['is_crawl']:
                            _followers = _post['followers']
                            for _follower in _followers:
                                _code = str(_user_profile['_id']) + '|' + str(_follower['user_id'])
                                _new_follower = {'_id': HashHelper.hash(_code),
                                                 'follower_id': _follower['user_id']}
                                if _fb_user_type == 'user':
                                    _new_follower['user_id'] = _user_profile['_id']
                                elif _fb_user_type == 'page':
                                    _new_follower['page_id'] = _user_profile['_id']
                                follower_objs.append([{'_id': _new_follower['_id']},
                                                      _new_follower])
        return follower_objs

    def _extract_newuser_data_from_reac(self,
                                        _user_infos):
        new_user_objs = []
        user_objs = []
        media_objs = []
        for _user_info in _user_infos:
            _user = _user_info['body']
            if _user_info['code'] == 200:
                _latest_posts = DictHelper.get_rfield(_dict=_user,
                                                      _field_names=['profile', 'latest_posts'],
                                                      _otherwise=[])
                for _post in _latest_posts:
                    if _post['is_crawl']:
                        _followers = _post['followers']
                        for _follower in _followers:
                            new_user_objs.append([{'_id': HashHelper.hash(str(_follower['user_id']))},
                                                  {'_id': HashHelper.hash(str(_follower['user_id'])),
                                                   'user_id': _follower['user_id'],
                                                   'username': _follower['username']}])
                            if 'mini_avatar' in _follower:
                                _link = _follower['mini_avatar']
                                _id = HashHelper.hash(_link + str(uuid.uuid4()))
                                _s3_link = AwsS3Helper.upload_image_to_s3_and_get_link(_image_url=_link,
                                                                                       _id=_id)
                                _media_obj = MediaModel.create_with(_link=_link, _s3_link=_s3_link)
                                media_objs.append([{'_id': _media_obj['_id']},
                                                   _media_obj])
                                user_objs.append([{'_id': _follower['user_id']},
                                                  {'_id': _follower['user_id'],
                                                   'username': _follower['username'],
                                                   'mini_avatar': _media_obj['_id']}
                                                  ])
        return new_user_objs, user_objs, media_objs

    def update_follower_from_reac_info_posts(self,
                                             _post_infos):
        # ===== Update follower =====
        _followers_objs = self._extract_follower_data_from_reac_post(_post_infos=_post_infos)
        self.userfollowuser_dbhandler.update_many_pair(_updated_records=_followers_objs,
                                                       _upsert=True)

        # ===== Update new users =====
        _normal_user_objs, \
        _user_objs, \
        _media_objs = self._extract_newuser_data_from_reac_post(_post_infos=_post_infos)
        if _normal_user_objs:
            # --- Parse info ---
            self.normaluser_dbhandler.find_or_create_many_pair(_updated_records=_normal_user_objs,
                                                               _upsert=True)
            self.user_dbhandler.update_many_pair(_updated_records=_user_objs,
                                                 _upsert=True)
            self.media_dbhandler.update_many_pair(_updated_records=_media_objs,
                                                  _upsert=True)
        # ===== Return value =====
        return 'success'

    def _extract_follower_data_from_reac_post(self,
                                              _post_infos):
        follower_objs = []
        for _post_info in _post_infos:
            _post = _post_info['body']
            if _post_info['code'] == 200:
                _user_id = DictHelper.get_field(_dict=_post,
                                                _field_name='user_id',
                                                _otherwise=None)
                _page_id = DictHelper.get_field(_dict=_post,
                                                _field_name='page_id',
                                                _otherwise=None)
                _user_profile_id = None
                _fb_user_type = None
                if _user_id > 0:
                    _user_profile_id = _user_id
                    _fb_user_type = 'user'
                elif _page_id:
                    _user_profile_id = _page_id
                    _fb_user_type = 'page'
                if _user_profile_id:
                    _followers = _post['followers']
                    for _follower in _followers:
                        _code = str(_user_profile_id) + '|' + str(_follower['user_id'])
                        _new_follower = {'_id': HashHelper.hash(_code),
                                         'follower_id': _follower['user_id']}
                        if _fb_user_type == 'user':
                            _new_follower['user_id'] = _user_profile_id
                        elif _fb_user_type == 'page':
                            _new_follower['page_id'] = _user_profile_id
                        follower_objs.append([{'_id': _new_follower['_id']},
                                              _new_follower])
        return follower_objs

    def _extract_newuser_data_from_reac_post(self,
                                             _post_infos):
        new_user_objs = []
        user_objs = []
        media_objs = []
        for _post_info in _post_infos:
            _post = _post_info['body']
            if _post_info['code'] == 200:
                _followers = _post['followers']
                for _follower in _followers:
                    new_user_objs.append([{'_id': HashHelper.hash(str(_follower['user_id']))},
                                          {'_id': HashHelper.hash(str(_follower['user_id'])),
                                           'user_id': _follower['user_id'],
                                           'username': _follower['username']}])
                    if 'mini_avatar' in _follower:
                        _link = _follower['mini_avatar']
                        _id = HashHelper.hash(_link + str(uuid.uuid4()))
                        _s3_link = AwsS3Helper.upload_image_to_s3_and_get_link(_image_url=_link,
                                                                               _id=_id)
                        _media_obj = MediaModel.create_with(_link=_link, _s3_link=_s3_link)
                        
                        media_objs.append([{'_id': _media_obj['_id']},
                                           _media_obj])
                        user_objs.append([{'_id': _follower['user_id']},
                                          {'_id': _follower['user_id'],
                                           'username': _follower['username'],
                                           'mini_avatar': _media_obj['_id']}
                                          ])
        return new_user_objs, user_objs, media_objs

    # endregion

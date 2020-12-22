# Import libs
import time  # Time lib

# Import Models
from DBService.Models.ReactionTypeEnum import ReactionTypeEnum
from DBService.Models.CrawlStatusEnum import CrawlStatusEnum
from DBService.Models.Media import MediaModel
from DBService.Models.DocStatusEnum import DocStatusEnum

# Import DBHandler
from DBService.DBHandler.UserDBHandler import UserDBHandler
from DBService.DBHandler.PageDBHandler import PageDBHandler
from DBService.DBHandler.PostDBHandler import PostDBHandler
from DBService.DBHandler.MediaDBHandler import MediaDBHandler
from DBService.DBHandler.KOLDBHandler import KOLDBHandler
from DBService.DBHandler.PostReactionDBHandler import PostReactionDBHandler
from DBService.DBHandler.PostCommentDBHandler import PostCommentDBHandler
from DBService.DBHandler.CommentDBHandler import CommentDBHandler

# Import Utils
from SuperUtils import DictHelper, DateHelper
from SuperUtils.HashHelper import HashHelper


class PostService(object):
    # ********** Constructor **********
    def __init__(self):
        self.post_dbhandler = PostDBHandler()
        self.user_dbhandler = UserDBHandler()
        self.page_dbhandler = PageDBHandler()
        self.kol_dbhandler = KOLDBHandler()
        self.media_dbhandler = MediaDBHandler()
        self.postreaction_dbhandler = PostReactionDBHandler()
        self.comment_dbhandler = CommentDBHandler()
        self.postcomment_dbhandler = PostCommentDBHandler()

    # region Get Posts

    # ********** Get Posts **********
    def get_post_by_post_id(self,
                            _post_id,
                            _selected_fields=None):
        result = self.post_dbhandler.get_one_by_post_id(_post_id=_post_id,
                                                        _selected_fields=_selected_fields)
        return result

    def get_posts_by_user_id_with_timerange(self,
                                            _user_id,
                                            _from,
                                            _to,
                                            _selected_fields=None):
        result = self.post_dbhandler.get_many_by_user_id_with_timerange(_user_id=_user_id,
                                                                        _from=_from,
                                                                        _to=_to,
                                                                        _selected_fields=_selected_fields)

        return result

    def get_posts_by_page_id_with_timerange(self,
                                            _page_id,
                                            _from,
                                            _to,
                                            _selected_fields=None):
        result = self.post_dbhandler.get_many_by_page_id_with_timerange(_page_id=_page_id,
                                                                        _from=_from,
                                                                        _to=_to,
                                                                        _selected_fields=_selected_fields)

        return result

    # endregion

    # region Change Comment Status

    def _change_comment_status_to(self,
                                  _posts,
                                  _comment_status,
                                  _save_current_time=False):
        if not _posts:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _post in _posts:
            _record = {'crawl_comment_status': _comment_status}
            if _save_current_time:
                _record['last_time_crawl_comment'] = _current_timestamp
            _updated_records.append([{'_id': _post['_id']},
                                     _record])
        service_result = self.post_dbhandler.update_many_pair(_updated_records=_updated_records)

        if service_result:
            return service_result
        return 'success'

    # ********** Change crawl_comment_status of posts to Crawling **********
    def change_comment_status_to_crawling(self,
                                          _posts):
        return self._change_comment_status_to(_posts=_posts,
                                              _comment_status=CrawlStatusEnum.Crawling)

    # ********** Change crawl_comment_status of posts to Unselected **********
    def change_comment_status_to_unselected(self,
                                            _posts):
        return self._change_comment_status_to(_posts=_posts,
                                              _comment_status=CrawlStatusEnum.Unselected,
                                              _save_current_time=True)

    # endregion

    # region Update Comments of Posts

    # ********** Update / Insert Comments of Posts **********
    def update_comment_info(self,
                            _post_infos):
        # ===== Insert post comment database =====
        for _post_info in _post_infos:
            _post = _post_info['body']
            if _post_info['code'] == 200:
                _post_comment_objs, \
                _reply_comment_objs, \
                _comment_objs = self._create_post_comment_objs(_post)
                if _post_comment_objs:
                    self.postcomment_dbhandler.update_many_pair(_updated_records=_post_comment_objs,
                                                                _upsert=True)
                    self.postcomment_dbhandler.update_many_pair(_updated_records=_reply_comment_objs,
                                                                _upsert=True)
                    self.comment_dbhandler.update_many_pair(_updated_records=_comment_objs,
                                                            _upsert=True)

                # --- Update score of the post ---
                self._update_comment_score_post(_post=_post)

        # ===== Update to DB =====
        # --- Update post ---
        _post_objs = self._extract_post_data_from_post(_post_infos=_post_infos)
        self.post_dbhandler.update_many_pair(_updated_records=_post_objs,
                                             _upsert=True)

    def _create_post_comment_objs(self,
                                  _post):
        post_comment_objs = []
        reply_comment_objs = []
        comment_objs = []
        _crawled_comments = _post['crawled_comments']
        for _crawled_comment in _crawled_comments:
            _code = str(_post['_id']) + '|' + _crawled_comment['id'] + '|' + str(_crawled_comment['user_id'])
            _post_comment_obj = {'_id': HashHelper.hash(_code),
                                 'post_id': _post['_id'],
                                 'comment_id': _crawled_comment['id'],
                                 'user_id': _crawled_comment['user_id']}
            if not _crawled_comment['parent_comment_id']:
                post_comment_objs.append([{'_id': _post_comment_obj['_id']},
                                          _post_comment_obj])
            else:
                reply_comment_objs.append([{'_id': _post_comment_obj['_id']},
                                           _post_comment_obj])

            _comment_obj = {}
            _comment_obj['post_id'] = _post['_id']
            DictHelper.transfer_fields(_crawled_comment, _comment_obj, ['id', 'fbid', 'parent_comment_id', 'message',
                                                                        'user_id', 'username', 'full_name',
                                                                        'num_reaction', 'taken_at_timestamp',
                                                                        'created_time',
                                                                        'sticker'])
            _comment_obj['_id'] = _comment_obj.pop('id', None)
            comment_objs.append([{'_id': _comment_obj['_id']},
                                 _comment_obj])

        # ===== Return post likes objects =====
        return post_comment_objs, reply_comment_objs, comment_objs

    def _update_comment_score_post(self,
                                   _post):
        if _post.get('num_comment') == 0 or _post.get('num_comment') is None:
            _post['num_crawled_comment'] = 0
            _post['crawl_comment_score'] = 1.0
        else:
            if 'num_crawled_comment' not in _post:
                _post['num_crawled_comment'] = 0
            if 'crawl_comment_score' not in _post:
                _post['crawl_comment_score'] = 0.0

            _num_first_level_comment = self._get_num_first_level_comment(_post_id=_post['_id'])
            _post['num_crawled_comment'] = _num_first_level_comment
            _post['crawl_comment_score'] = _post['num_crawled_comment'] * 1.0 / _post['num_comment']

    def _get_num_first_level_comment(self,
                                     _post_id):
        num_first_level_comment = 0

        _crawled_comments = self.comment_dbhandler.get_comments_by_post_id(_post_id=_post_id,
                                                                           _selected_fields=['parent_comment_id'])
        for _comment in _crawled_comments:
            _parent_id = DictHelper.get_field(_dict=_comment, _field_name='parent_comment_id', _otherwise=None)
            if _parent_id is None or _parent_id == '':
                num_first_level_comment += 1

        return num_first_level_comment

    def _extract_post_data_from_post(self,
                                     _post_infos):
        post_objs = []

        for _post_info in _post_infos:
            _post = _post_info['body']
            if _post_info['code'] == 200:
                _post_obj = {}
                DictHelper.transfer_fields(_post, _post_obj, ['_id',
                                                              'num_crawled_comment',
                                                              'crawl_comment_score',
                                                              'comment_info'])
                _post_obj['comment_info']['reach_end'] = bool(_post_obj['comment_info']['offset'] == 0)
                post_objs.append([{'_id': _post_obj['_id']},
                                  _post_obj])

        return post_objs

    # endregion

    # ********** Get posts by id **********
    def get_post_by_id(self,
                       _post_id,
                       _selected_fields=None):
        result = self.post_dbhandler.get_one_by_id(_id=_post_id,
                                                   _selected_fields=_selected_fields)
        return result

    def get_posts_by_id(self,
                        _post_ids,
                        _selected_fields=None):
        result = self.post_dbhandler.get_many_pairs_by_id(_ids=_post_ids,
                                                          _selected_fields=_selected_fields)
        return result

    # region Update Reaction of Users | Posts

    # ********** Update / Insert Posts **********
    def update_reaction_info_of_users(self,
                                      _user_infos):
        # ===== Insert post like database =====
        for _user_info in _user_infos:
            _user = _user_info['body']
            if _user_info['code'] == 200:
                _latest_posts = DictHelper.get_rfield(_dict=_user,
                                                      _field_names=['profile', 'latest_posts'],
                                                      _otherwise=[])
                for _post in _latest_posts:
                    if _post['is_crawl']:
                        _post_reaction_objs = self._create_post_reaction_objs(_post)
                        if _post_reaction_objs:
                            _postreaction_result = self.postreaction_dbhandler.update_many_pair(
                                _updated_records=_post_reaction_objs,
                                _upsert=True)
                        else:
                            _postreaction_result = None
                        _post['reaction_result'] = _postreaction_result

                        # --- Update score of the post ---
                        self._update_reaction_score_post(_post=_post)

                # --- Update score of the user ---
                self._update_reaction_score_user(_user=_user)

        # ===== Update to DB =====
        # --- Update post ---
        _post_objs = self._extract_reac_post_data_from_user(_user_infos=_user_infos)
        self.post_dbhandler.update_many_pair(_updated_records=_post_objs,
                                             _upsert=True)

        # --- Update user ---
        _user_objs, \
        _page_objs = self._extract_user_data(_user_infos=_user_infos)
        self.user_dbhandler.update_many_pair(_updated_records=_user_objs,
                                             _upsert=True)
        self.page_dbhandler.update_many_pair(_updated_records=_page_objs,
                                             _upsert=True)

        # ===== Return value =====
        return 'success'

    # ********** Update / Insert Posts **********
    def update_reaction_info_of_posts(self,
                                      _post_infos):
        # ===== Insert post like database =====
        for _post_info in _post_infos:
            _post = _post_info['body']
            if _post_info['code'] == 200:
                _post_reaction_objs = self._create_post_reaction_objs(_post=_post)
                if _post_reaction_objs:
                    _postreaction_result = self.postreaction_dbhandler.update_many_pair(
                        _updated_records=_post_reaction_objs,
                        _upsert=True)
                else:
                    _postreaction_result = None
                _post['reaction_result'] = _postreaction_result

                # --- Update score of the post ---
                self._update_reaction_score_post(_post=_post)

        # ===== Update to DB =====
        # --- Update post ---
        _post_objs = self._extract_reac_post_data_from_post(_post_infos=_post_infos)
        self.post_dbhandler.update_many_pair(_updated_records=_post_objs,
                                             _upsert=True)

        # ===== Return value =====
        return 'success'

    def _create_post_reaction_objs(self,
                                   _post):
        post_reaction_objs = []
        _followers = _post['followers']
        for _follower in _followers:
            _code = str(_post['_id']) + '|' + str(_follower['user_id'])
            post_reaction_objs.append([{'_id': HashHelper.hash(_code)},
                                       {'_id': HashHelper.hash(_code),
                                        'post_id': _post['_id'],
                                        'user_id': _follower['user_id'],
                                        'type': ReactionTypeEnum.parse_type(_follower['type'])}])

        # ===== Return post likes objects =====
        return post_reaction_objs

    def _update_reaction_score_post(self,
                                    _post):
        _post_id = _post['_id']
        if _post.get('num_reaction') is None or _post.get('num_reaction') == 0:
            _post['num_crawled_reaction'] = 0
            _post['crawl_reaction_score'] = 1.0
        else:
            if 'num_crawled_reaction' not in _post:
                _post['num_crawled_reaction'] = 0
            if 'crawl_reaction_score' not in _post:
                _post['crawl_reaction_score'] = 0.0

            _can_load_page = DictHelper.get_field(_dict=_post, _field_name='can_load_page', _otherwise=True)
            if _can_load_page:
                _num_crawled_reaction = self.postreaction_dbhandler.get_many_by_filter(
                    _filter={'post_id': _post_id}).count()
                _post['num_crawled_reaction'] = _num_crawled_reaction
                _post['crawl_reaction_score'] = _post['num_crawled_reaction'] * 1.0 / _post['num_reaction']
            else:
                _post['crawl_reaction_score'] = 1.0

    def _update_reaction_score_user(self,
                                    _user):
        _posts = DictHelper.get_rfield(_dict=_user,
                                       _field_names=['profile', 'latest_posts'],
                                       _otherwise=[])
        if 'crawl_reaction_score' not in _user:
            _user['crawl_reaction_score'] = 0.0

        if _posts:
            _user_reaction_score = sum([_post['crawl_reaction_score']
                                        for _post in _posts]) / len(_posts)
            _user['crawl_reaction_score'] = _user_reaction_score
        else:
            _user_reaction_score = 1.0
            _user['crawl_reaction_score'] = _user_reaction_score

    def _extract_reac_post_data_from_user(self,
                                          _user_infos):
        post_objs = []
        for _user_info in _user_infos:
            _user = _user_info['body']
            if _user_info['code'] == 200:
                _latest_posts = DictHelper.get_rfield(_dict=_user,
                                                      _field_names=['profile', 'latest_posts'],
                                                      _otherwise=[])
                for _post in _latest_posts:
                    _new_record = {}
                    DictHelper.transfer_fields(_post, _new_record, ['num_crawled_reaction',
                                                                    'crawl_reaction_score',
                                                                    'reaction_info'])
                    post_objs.append([{'_id': _post['_id']},
                                      _new_record])
        return post_objs

    def _extract_reac_post_data_from_post(self,
                                          _post_infos):
        post_objs = []
        for _post_info in _post_infos:
            _post = _post_info['body']
            if _post_info['code'] == 200:
                _new_record = {}
                DictHelper.transfer_fields(_from=_post,
                                           _to=_new_record,
                                           _fields=['num_crawled_reaction',
                                                    'crawl_reaction_score',
                                                    'reaction_info'])
                post_objs.append([{'_id': _post['_id']},
                                  _new_record])
        return post_objs

    def _extract_user_data(self,
                           _user_infos):
        user_objs = []
        page_objs = []
        for _user_info in _user_infos:
            _user = _user_info['body']
            if _user_info['code'] == 200:
                if 'crawl_reaction_score' in _user:
                    _user_obj = [{'_id': _user['_id']},
                                 {'crawl_reaction_score': _user['crawl_reaction_score']}]
                    if _user['fb_user_type'] == 'user':
                        user_objs.append(_user_obj)
                    elif _user['fb_user_type'] == 'page':
                        page_objs.append(_user_obj)

        return user_objs, page_objs

    # endregion

    # region Update Latest Post of Users

    def _extract_latest_posts(self, _kols,
                              _post_infos):
        # ===== Extract Media | Education | Work | Location =====
        media_objs = []
        post_objs = []

        for _kol_posts in _post_infos:
            if _kol_posts['body'] != {}:
                list_posts = _kol_posts['body']['posts']
                print(_kol_posts['code'])
                _profile_add_id = _kol_posts['profile']

                if _kol_posts['code'] == 200:
                    _latest_posts = list_posts
                    _media_objs, \
                    _post_objs = self._extract_posts(_posts=_latest_posts, _profile_user=_profile_add_id, _kols=_kols)
                    media_objs += _media_objs
                    post_objs += _post_objs

        # print(post_objs)
        # ===== Extract profile =====
        user_objs = []
        page_objs = []
        kols_objs = []
        for _kol_posts in _post_infos:
            if _kol_posts['body'] != {}:
                _profile = _kol_posts['profile']
                profile = _profile if _profile != 'kol' else _kols
                list_posts = _kol_posts['body']['posts']
                # print(_profile)
                # print(_kol_posts['profile']['hiip_user_type'])
                _post_type = profile['hiip_user_type']

                if _kol_posts['code'] == 200:
                    """check status_code"""

                    # get old post by user_id or page_id

                    # print(_kol_obj)
                    if _post_type == 'user':
                        user_id = profile['user_id']

                        if user_id is not None and user_id > 0:
                            _kol_obj = {'crawl_post_code': _kol_posts['code']}

                            user_objs.append([{'_id': profile['user_id']}, _kol_obj])
                        else:
                            _user_obj = {
                                '_id': profile['app_id'],
                                'app_id': profile['app_id'],
                                'crawl_post_code': _kol_posts['code']
                            }

                            _kols_update = {
                                'user_id': profile['app_id']
                            }
                            print("Update app_id into user_id field in kols collection")
                            kols_objs.append([{'_id': profile['_id']}, _kols_update])
                            user_objs.append([{'_id': profile['app_id']}, _user_obj])

                    if _post_type == 'page':
                        print(profile)
                        # get latest_post from page
                        _kol_obj = {'crawl_post_code': _kol_posts['code']}
                        page_objs.append([{'_id': list_posts[0]['post_detail']['from']['id']},
                                          _kol_obj])

        # print(str(media_objs).encode('utf-8'))
        # print(str(post_objs).encode('utf-8'))
        # print(str(page_objs).encode('utf-8'))
        # print(str(user_objs).encode('utf-8'))
        return user_objs, page_objs, media_objs, post_objs, kols_objs

    def _extract_posts(self,
                       _posts, _profile_user, _kols):
        media_objs = []
        post_objs = []
        print(_profile_user)
        profile_user = _profile_user if _profile_user != 'kol' else _kols
        # print(str(_profile_user).encode('utf-8'))
        for _post in _posts:
            # print(str(_post).encode('utf-8'))
            # --- Parse media ---
            if 'status' in _post and _post['status'] == 'SUCCESS':
                _post_detail = _post['post_detail']
                if 'full_picture' in _post_detail:
                    _media_obj = MediaModel.create_with(_link=_post_detail['full_picture'])
                    media_objs.append([{'_id': _media_obj['_id']},
                                       _media_obj])
                    _post_detail['full_picture'] = _media_obj['_id']

                if profile_user['hiip_user_type'] == 'user' and \
                        (profile_user['user_id'] is None or profile_user['user_id'] < 0):
                    _post_detail['user_id'] = profile_user['app_id']
                elif profile_user['hiip_user_type'] == 'user' and profile_user['user_id'] > 0:
                    _post_detail['user_id'] = profile_user['user_id']
                elif profile_user['hiip_user_type'] == 'page':
                    _post_detail['page_id'] = _post_detail['from']['id']

                if '_id' in _post_detail:
                    post_objs.append([{'_id': _post_detail['_id']},
                                      _post_detail])
        # print(media_objs)
        # print(post_objs)
        return media_objs, post_objs

    def update_post_infos(self, _kols, _post_infos):
        # ===== Insert into database =====
        _user_objs, \
        _page_objs, \
        _media_objs, \
        _post_objs, \
        _kol_objs = self._extract_latest_posts(_kols, _post_infos)

        # === Insert media ===
        # print("=== Insert media ===")
        self.media_dbhandler.update_many_pair(_updated_records=_media_objs,
                                              _upsert=True)

        # === Insert post ===
        # print("=== Insert post ===")
        self.post_dbhandler.update_many_pair(_updated_records=_post_objs,
                                             _upsert=True)

        # === Insert users ===
        # --- Update latest post by query from database
        user_objs = self.extract_latest_post_from_db(user_objs=_user_objs)

        # print("=== Insert users ===")
        self.user_dbhandler.update_many_pair(_updated_records=user_objs,
                                             _upsert=True)

        # === Insert pages ===
        # --- Update latest post by query from database
        page_objs = self.extract_latest_post_page_from_db(page_objs=_page_objs)

        # print("=== Insert pages ===")
        self.page_dbhandler.update_many_pair(_updated_records=page_objs,
                                             _upsert=True)

        # === Insert pages ===
        # print("=== Insert pages ===")
        self.kol_dbhandler.update_many_pair(_updated_records=_kol_objs,
                                            _upsert=True)
        print("=== Insert to DB Done ===")
        # Update KOLs Collection

        # For each case -> page_url exits or not
        # ===== Return value =====
        return 'success'

    # Extract latest_post from database
    def extract_latest_post_from_db(self, user_objs):
        """Extract latest post from db after store crawled Post"""
        for _user in user_objs:
            # get list latest post
            user_id = int(_user[0]['_id'])
            _filter = {
                'user_id': user_id
            }
            _sort = [("taken_at_timestamp", -1)]
            _latest_post = self.post_dbhandler.get_many_by_user_id(_filter=_filter,
                                                                   _sort=_sort,
                                                                   _selected_fields=['_id'],
                                                                   _num_post=30)
            latest_post = [post['_id'] for post in _latest_post]
            _user[1]['latest_posts'] = latest_post
            _user[0]['_id'] = user_id
            _user[1]['_id'] = user_id
            print(_user[1]['latest_posts'])
        return user_objs

    # Extract latest_post from database
    def extract_latest_post_page_from_db(self, page_objs):
        """Extract latest post from db after store crawled Post"""
        res_user_objs = []
        for _page in page_objs:
            # get list latest post
            page_id = _page[0]['_id']
            _filter = {
                'page_id': page_id
            }
            _sort = [("taken_at_timestamp", -1)]
            _latest_post = self.post_dbhandler.get_many_by_user_id(_filter=_filter,
                                                                   _sort=_sort,
                                                                   _selected_fields=['_id'],
                                                                   _num_post=30)
            latest_post = [post['_id'] for post in _latest_post]
            _page[1]['latest_posts'] = latest_post
            _page[0]['_id'] = page_id
            _page[1]['_id'] = page_id
            print(_page[1]['latest_posts'])
            res_user_objs.append(_page)
        return res_user_objs

    # endregion

    # region Change Viewcount Status

    def _change_view_count_status_to(self,
                                     _posts,
                                     _view_count_status,
                                     _save_current_time=False):
        if not _posts:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _post in _posts:
            _record = {'crawl_view_count_status': _view_count_status}
            if _save_current_time:
                _record['last_time_crawl_view_count'] = _current_timestamp
            _updated_records.append([{'_id': _post['_id']},
                                     _record])
        service_result = self.post_dbhandler.update_many_pair(_updated_records=_updated_records)

        if service_result:
            return service_result
        return 'success'

    # ********** Change crawl_view_count_status of posts to Pending **********
    def change_view_count_status_to_pending(self,
                                            _posts):
        return self._change_view_count_status_to(_posts=_posts,
                                                 _view_count_status=CrawlStatusEnum.Pending)

    # ********** Change crawl_view_count_status of posts to Crawling **********
    def change_view_count_status_to_crawling(self,
                                             _posts):
        return self._change_view_count_status_to(_posts=_posts,
                                                 _view_count_status=CrawlStatusEnum.Crawling)

    # ********** Change crawl_view_count_status of posts to Crawled **********
    def change_view_count_status_to_crawled(self,
                                            _posts):
        return self._change_view_count_status_to(_posts=_posts,
                                                 _view_count_status=CrawlStatusEnum.Crawled,
                                                 _save_current_time=True)

    # endregion

    # region Update View Count Post

    def update_view_count_posts(self,
                                _post_infos):
        _post_objs = []
        for _post_info in _post_infos:
            _post = _post_info['body']
            if _post_info['code'] == 200:
                _post_objs.append([{'_id': _post['_id']},
                                   _post])
        service_result = self.post_dbhandler.update_many_pair(_updated_records=_post_objs,
                                                              _upsert=False)
        return service_result

    # endregion

    # region Change reaction Status

    def _change_reaction_status_to(self,
                                   _posts,
                                   _reaction_status,
                                   _save_current_time=False):
        if not _posts:
            return 'success'

        _updated_records = []
        _current_timestamp = DateHelper.current_itimestamp()
        for _post in _posts:
            _record = {'crawl_reaction_status': _reaction_status}
            if _save_current_time:
                _record['last_time_crawl_reaction'] = _current_timestamp
            _updated_records.append([{'_id': _post['_id']},
                                     _record])
        service_result = self.post_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    # ********** Change crawl_reaction_status of posts to Crawling **********
    def change_reaction_status_to_crawling(self,
                                           _posts):
        return self._change_reaction_status_to(_posts=_posts,
                                               _reaction_status=DocStatusEnum.Crawling)

    # ********** Change crawl_reaction_status of posts to Unselected **********
    def change_reaction_status_to_unselected(self,
                                             _posts):
        return self._change_reaction_status_to(_posts=_posts,
                                               _reaction_status=DocStatusEnum.Unselected,
                                               _save_current_time=True)

    def check_type_of_post(self, post_app_id):
        """
        Check type of post (page /user)

        Input:
        - post_app_id (str / int): Post app id from report

        Output:
        - post_type (str): Type of post (page / user)
        """
        if isinstance(post_app_id, str):
            result = self.post_dbhandler.collection.find_one({"app_id": post_app_id})
        else:
            result = self.post_dbhandler.collection.find_one({"_id": post_app_id})
        post_type = "page" if result and result.get('page_id') else "user"
        return post_type


    # endregion

# Import libs
import time  # Time lib

# Import Models
from DBService.Models.CrawlStatusEnum import CrawlStatusEnum

# Import DBHandler
from DBService.DBHandler.PageDBHandler import PageDBHandler

# Import Utils
from SuperUtils import DictHelper
from SuperUtils.HashHelper import HashHelper


class PageService(object):
    # ********** Constructor **********
    def __init__(self):
        self.page_dbhandler = PageDBHandler()

    # ********** Get Page(s) by id **********
    def get_page_by_id(self,
                       _page_id,
                       _selected_fields=None):
        result = self.page_dbhandler.get_one_by_id(_id=_page_id,
                                                   _selected_fields=_selected_fields)
        return result

    def get_pages_by_id(self,
                        _page_ids,
                        _filter=None,
                        _selected_fields=None,
                        _must_have_fields=None,
                        _not_have_fields=None):
        result = self.page_dbhandler.get_many_pairs_by_id(_ids=_page_ids,
                                                          _filter=_filter,
                                                          _selected_fields=_selected_fields,
                                                          _must_have_fields=_must_have_fields,
                                                          _not_have_fields=_not_have_fields)
        return result

    # region Change Profile Status

    def _change_profile_status_to(self,
                                  _pages,
                                  _profile_status,
                                  _save_current_time=False):
        if not _pages:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _page in _pages:
            _record = {'crawl_profile_status': _profile_status}
            if _save_current_time:
                _record['last_time_crawl_profile'] = _current_timestamp
            _updated_records.append([{'_id': _page['_id']},
                                     _record])
        service_result = self.page_dbhandler.update_many_pair(_updated_records=_updated_records)

        if service_result:
            return service_result
        return 'success'

    # ********** Change crawl_profile_status of pages to Crawling **********
    def change_profile_status_to_crawling(self,
                                          _pages):
        return self._change_profile_status_to(_pages=_pages,
                                              _profile_status=CrawlStatusEnum.Crawling)

    # ********** Change crawl_profile_status of pages to Crawled **********
    def change_profile_status_to_crawled(self,
                                         _pages):
        return self._change_profile_status_to(_pages=_pages,
                                              _profile_status=CrawlStatusEnum.Crawled,
                                              _save_current_time=True)

    # endregion

    # region Update Profile of (Normal) Page

    def update_profile_info_pages(self,
                                  _page_infos):
        # ===== Insert into database =====
        _page_objs = self._extract_page(_page_infos)

        # === Insert media ===
        self.page_dbhandler.update_many_pair(_updated_records=_page_objs,
                                             _upsert=True)

        # ===== Return value =====
        return 'success'

    def _extract_page(self,
                      _page_infos):
        page_objs = []
        for _page_info in _page_infos:
            _page = _page_info['body']
            _page_obj = {}
            _page_obj['crawl_profile_code'] = _page_info['code']
            DictHelper.transfer_fields(_page, _page_obj, ['_id', 'app_id', 'username', 'about',
                                                          'bio', 'fb_link', 'category', 'category_list',
                                                          'fan_count', 'location', 'band_interests', 'influences',
                                                          'page_url'])
            page_objs.append([{'_id': _page_obj['_id']},
                              _page_obj])
        return page_objs

    # endregion

    # region Update Profile of KOL Page

    def update_profile_info_kol_pages(self,
                                      _page_infos):
        # ===== Insert into database =====
        _page_objs = self._extract_kol_page(_page_infos)

        # === Insert media ===
        self.page_dbhandler.update_many_pair(_updated_records=_page_objs,
                                             _upsert=True)
        # ===== Return value =====
        return 'success'

    def _extract_kol_page(self,
                          _page_infos):
        page_objs = []
        for _page_info in _page_infos:
            _page = _page_info['body']
            _page_obj = {}
            _page_obj['crawl_profile_code'] = _page_info['code']
            DictHelper.transfer_fields(_page, _page_obj, ['_id', 'app_id', 'username', 'about',
                                                          'bio', 'fb_link', 'category', 'category_list',
                                                          'fan_count', 'location', 'band_interests', 'influences',
                                                          'page_url'])
            _page_id = None
            if 'page_url' in _page:
                _page_id = HashHelper.hash(_page['page_url'])
            elif 'app_id' in _page:
                _page['page_url'] = 'https://www.facebook.com/%d' % _page['app_id']
                _page_id = HashHelper.hash(_page['page_url'])

            if '_id' in _page_obj:
                _page_obj['_id'] = _page_id
            page_objs.append([{'_id': _page_id},
                              _page_obj])

        return page_objs

    # endregion

    # region Change Post Status

    def _change_post_status_to(self,
                               _pages,
                               _post_status,
                               _save_current_time=False):
        if not _pages:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _page in _pages:
            _record = {'crawl_post_status': _post_status}
            if _save_current_time:
                _record['last_time_crawl_post'] = _current_timestamp
            _updated_records.append([{'_id': _page['_id']},
                                     _record])
        service_result = self.page_dbhandler.update_many_pair(_updated_records=_updated_records)

        if service_result:
            return service_result
        return 'success'

    # ********** Change crawl_post_status of users to Crawling **********
    def change_post_status_to_crawling(self,
                                       _pages):
        return self._change_post_status_to(_pages=_pages,
                                           _post_status=CrawlStatusEnum.Crawling)

    # ********** Change crawl_post_status of users to Crawled **********
    def change_post_status_to_crawled(self,
                                      _pages):
        return self._change_post_status_to(_pages=_pages,
                                           _post_status=CrawlStatusEnum.Crawled,
                                           _save_current_time=True)

    # endregion

# Import libs
import time

# Import model
from datetime import date

from DBService.Models.ReportStatusEnum import ReportStatusEnum
from DBService.Models.CrawlStatusEnum import CrawlStatusEnum
from DBService.Models.Media import MediaModel
from DBService.Models.StatusEnum import StatusEnum

# Import DBHandler
from DBService.DBHandler.ReportDBHandler import ReportDBHandler
from DBService.DBHandler.PostDBHandler import PostDBHandler
from DBService.DBHandler.MediaDBHandler import MediaDBHandler

# Import utils
from SuperUtils import DictHelper


class ReportService(object):
    # ********** Constructor **********
    def __init__(self):
        self.report_dbhandler = ReportDBHandler()
        self.post_dbhandler = PostDBHandler()
        self.media_dbhandler = MediaDBHandler()

    def get_report_sort(self, _filter, _sort, _num_kol=20):
        result = self.report_dbhandler \
            .get_many_by_filter_and_sort(_filter=_filter,
                                         _sort=_sort,
                                         _selected_fields=['_id', 'username', 'report_type', 'post_time_to',
                                                           'post_time_from',
                                                           'hiip_post_id', 'post_content', 'post_id']) \
            .limit(_num_kol)
        return result

    def get_report_sort_selected_fields(self, _filter, _sort, _selected_fields, _num_kol=20):
        result = self.report_dbhandler \
            .get_many_by_filter_and_sort(_filter=_filter,
                                         _sort=_sort,
                                         _selected_fields=_selected_fields) \
            .limit(_num_kol)
        return result

    def get_reports_by_id(self,
                          _ids,
                          _selected_fields=None):
        result = self.report_dbhandler.get_many_pairs_by_id(_ids=_ids,
                                                            _selected_fields=_selected_fields)
        return result

    def store_new_engagement_report(self,
                                    report_objs):
        if report_objs:
            self.report_dbhandler.update_many_pair(_updated_records=report_objs)

    # region Change Post Status

    def _change_post_status_to(self,
                               _reports,
                               _post_status,
                               _save_current_time=False):
        if not _reports:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _report in _reports:
            _record = {'crawl_post_status': _post_status}
            if _save_current_time:
                _record['last_time_crawl_post'] = _current_timestamp
            _updated_records.append([{'_id': _report['_id']},
                                     _record])
        service_result = self.report_dbhandler.update_many_pair(_updated_records=_updated_records)
        return service_result

    # ********** Change crawl_post_status of reports to Crawling **********
    def change_post_status_to_crawling(self, _reports):
        return self._change_post_status_to(_reports=_reports,
                                           _post_status=CrawlStatusEnum.Crawling)

    # ********** Change crawl_post_status of reports to Crawled **********
    def change_post_status_to_crawled(self, _reports):
        return self._change_post_status_to(_reports=_reports,
                                           _post_status=CrawlStatusEnum.Crawled,
                                           _save_current_time=True)

    def change_tracking_status_to_failed(self,
                                         _reports):
        return self._change_tracking_status_to(_reports=_reports,
                                               _tracking_status=ReportStatusEnum.Failed)

    def change_tracking_status_to_missing(self,
                                          _reports):
        return self._change_tracking_status_to(_reports=_reports,
                                               _tracking_status=ReportStatusEnum.Missing)

    def _change_tracking_status_to(self,
                                   _reports,
                                   _tracking_status,
                                   _save_current_time=False):
        if not _reports:
            return 'success'

        _updated_records = []
        _current_timestamp = int(time.time())
        for _report in _reports:
            _record = {'tracking_status': _tracking_status}
            if _save_current_time:
                _record['last_time_tracking'] = _current_timestamp
            _updated_records.append([{'_id': _report['_id']},
                                     _record])
        service_result = self.report_dbhandler.update_many_pair(_updated_records=_updated_records)

        return service_result

    # endregion

    # region update report post of user
    def update_post_info_reports(self, _report_infos):
        # extract data
        _report_objs, _post_objs, _media_objs = self._extract_post_report_infos(_report_infos=_report_infos)

        # save data
        if _post_objs:
            self.post_dbhandler.update_many_pair(_updated_records=_post_objs, _upsert=True)

        if _media_objs:
            self.media_dbhandler.update_many_pair(_updated_records=_media_objs, _upsert=True)

        if _report_objs:
            self.report_dbhandler.update_many_pair(_updated_records=_report_objs)

    def _extract_post_report_infos(self, _report_infos):
        report_objs = []
        post_objs = []
        media_objs = []

        for _info in _report_infos:
            _report = _info['body']
            if _info['code'] == 200:
                _post = DictHelper.get_field(_dict=_report, _field_name='post', _otherwise=None)
                if _report['status'] == StatusEnum.Yes:
                    if _post:
                        _media_objs_ii, \
                        _post_objs_ii = self._extract_report_post(_post=_post)

                        media_objs += _media_objs_ii
                        post_objs += _post_objs_ii

                        # report
                        if _report['save_post_id'] == StatusEnum.Yes:
                            _report_obj = {
                                'post_id': _post['post_id']
                            }
                            report_objs.append([{'_id': _report['_id']},
                                                _report_obj])

        return report_objs, post_objs, media_objs

    def _extract_report_post(self,
                             _post):
        media_objs = []
        post_objs = []

        # --- Parse media ---
        if 'full_picture' in _post:
            _media_obj = MediaModel.create_with(_link=_post['full_picture'])
            media_objs.append([{'_id': _media_obj['_id']},
                               _media_obj])
            _post['full_picture'] = _media_obj['_id']

        # --- Parse post ---
        _post_obj = {}
        DictHelper.transfer_fields(_from=_post,
                                   _to=_post_obj,
                                   _fields=['app_id',
                                            'content', 'story',
                                            'post_type', 'status_type',
                                            'page_url', 'link', 'permalink',
                                            'user_id', 'page_id',
                                            'view_count', 'num_reaction', 'num_comment', 'num_share', 'has_view_count',
                                            'taken_at_timestamp', 'created_time',
                                            'full_picture'])
        if 'post_id' in _post:
            _post_obj['_id'] = _post['post_id']
            post_objs.append([{'_id': _post_obj['_id']},
                              _post_obj])

        return media_objs, post_objs

    def update_history_report(self, _selected_reports):
        # Get post info
        for report in _selected_reports:
            # print(report['post_id'])
            if 'post_id' in report:
                post_id = report['post_id']
                post_info = self.post_dbhandler.get_one_by_post_id(
                    _post_id=report['post_id'],
                    _selected_fields=['_id', 'app_id', 'num_comment', 'num_reaction', 'num_share'])

                print(post_info)
                report_objs = []
                current_date = date.today().strftime("%Y-%m-%d")
                current_time = int(time.time())
                print(report['post_id'])
                _report_obj = {
                    'post_id': post_id,
                    'last_time_checking': current_time,
                    'last_time_report_engagement': current_time,
                    'tracking_status': 'Tracking'
                }
                _report_obj['post_app_id'] = post_info['app_id']
                _report_obj['history_report.' + str(current_date)] = {
                    'num_comment': post_info['num_comment'],
                    'num_like': post_info['num_reaction'],
                    'taken_at_timestamp': current_time
                }
                report_objs.append([{'_id': report['_id']},
                                    _report_obj])
                self.store_new_engagement_report(report_objs=report_objs)

    def update_crawl_comment_status_to(self, _report, crawl_status, crawl_code):
        """
        Update crawl comment "status" for report into collection "reports"

        Input:
        - _report (dict): Report info
        - crawl_status (str): Status of crawl comment process
        - crawl_code (int): Status code of crawl comment process
        """
        if not _report:
            return 'success'
        update_document = {
            "crawl_comment_status": crawl_status,
            "crawl_comment_code": crawl_code,
            "last_time_crawl_comment": int(time.time())
        }
        service_result = self.report_dbhandler.collection.update_one({
            "hiip_post_id": _report['hiip_post_id'],
            "country_code": _report['country_code'],
        }, {"$set": update_document})
        return service_result
    # endregion

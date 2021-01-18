from core.utils.constant import Constant
from workflow.loading.query.base_query import Query


class ReportQuery:
    @staticmethod
    def get_report_service_query(service_config: dict):
        filter_ = {
            'social_type': Constant.SOCIAL_TYPE_PROFILE,
            'country_code': {'$in': service_config.get('MARKET')},
            'search_report_status.status': {'$nin': ['success']},
        }
        filter_.pop('country_code') if not service_config.get('MARKET') else None
        sort_ = [("search_report_status.latest_update_time", 1)]
        limit_ = 10
        selected_fields = ['_id', 'username', 'report_type', 'user_id', 'user_app_id', 'country_code',
                           'post_time_from', 'post_time_to', 'post_content', 'hiip_post_id', 'post_id', 'post_link']

        return Query(filter_=filter_, sort_=sort_, limit_=limit_, selected_fields=selected_fields, priority=1)

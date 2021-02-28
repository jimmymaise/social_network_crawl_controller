import time

from core.workflows.loading.query.base_query import Query
from social_networks.tiktok.utils.constant import Constant


class ReportQuery:
    @staticmethod
    def get_kols_for_user_collection_service(service_config: dict):
        maximum_days_after_taken = Constant.DEFAULT_MAXIMUM_DAYS_AFTER_TAKEN
        maximum_seconds_after_taken = maximum_days_after_taken * Constant.TIME_ONE_DAY_TO_SECONDS
        current_timestamp = int(time.time())

        filter_ = {
            'country_code': {'$in': service_config.get('MARKET')},
            'taken_at_timestamp': {'$gt': current_timestamp - maximum_seconds_after_taken},
            f'{service_config["SERVICE_NAME"]}_status.status': {'$nin': ['success']},
        }
        filter_.pop('country_code') if not service_config.get('MARKET') else None
        sort_ = [(f'{service_config["SERVICE_NAME"]}_status.latest_update_time', 1)]
        limit = Constant.DEFAULT_LOAD_LIMIT_NUM_ITEM
        return Query(filter_=filter_, sort_=sort_, limit=limit, selected_fields=[], priority=1)

    @staticmethod
    def get_reports_for_comment_report_service(service_config: dict):
        maximum_days_after_taken = Constant.DEFAULT_MAXIMUM_DAYS_AFTER_TAKEN
        maximum_seconds_after_taken = maximum_days_after_taken * Constant.TIME_ONE_DAY_TO_SECONDS
        current_timestamp = int(time.time())

        filter_ = {
            'country_code': {'$in': service_config.get('MARKET')},
            'taken_at_timestamp': {'$gt': current_timestamp - maximum_seconds_after_taken},
            f'{service_config["SERVICE_NAME"]}_status.status': {'$nin': ['success', 'wait_search']},
        }
        filter_.pop('country_code') if not service_config.get('MARKET') else None
        sort_ = [(f'{service_config["SERVICE_NAME"]}_status.latest_update_time', 1)]
        limit = Constant.DEFAULT_LOAD_LIMIT_NUM_ITEM
        return Query(filter_=filter_, sort_=sort_, limit=limit, selected_fields=[], priority=1)

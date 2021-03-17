from core.workflows.loading.query.base_query import Query
from social_networks.tiktok.utils.constant import Constant


class KOLQuery:
    @staticmethod
    def get_kols_for_user_collection_service(service_config: dict):
        filter_ = {
            'country_code': {'$in': service_config.get('MARKET')},
            f'{service_config["SERVICE_NAME"]}_status.status': {'$nin': ['success']},
        }
        filter_.pop('country_code') if not service_config.get('MARKET') else None
        sort_ = [(f'{service_config["SERVICE_NAME"]}_status.latest_update_time', 1)]
        limit = Constant.DEFAULT_LOAD_LIMIT_NUM_ITEM
        return Query(filter_=filter_, sort_=sort_, limit=limit, selected_fields=[], priority=1)

    @staticmethod
    def get_kols_for_posts_collection_service(service_config: dict):
        filter_ = {
            'country_code': {'$in': service_config.get('MARKET')},
            f'user_collection_status.status': 'success',
            f'post_list_collection_status.status': {'$in': ['success', 'new']}
        }
        filter_.pop('country_code') if not service_config.get('MARKET') else None
        sort_ = [(f'posts_collection_status.latest_update_time', 1)]
        limit = Constant.DEFAULT_LOAD_LIMIT_NUM_ITEM
        selected_fields = ['_id', 'username']
        return Query(filter_=filter_, sort_=sort_, limit=limit, selected_fields=selected_fields, priority=1)

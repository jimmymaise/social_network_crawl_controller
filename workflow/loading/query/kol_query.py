import time

from workflow.loading.query.base_query import Query


class KOLQuery:
    @staticmethod
    def get_identity_query(service_config: dict):
        filter_ = {
            'crawl_identity_status': {'$nin': ['Failed']},
            'hiip_user_type': {'$in': ['user', 'page']},
            'country_code': {'$in': service_config['MARKET']},
            '$or': [{'influencer_type': {'$nin': ['INFLUENCE_TYPE_IGNORE']}},
                    {'influencer_type': {'$exists': False}}],
            'last_time_crawl_identity': {'$lte': (time.time() - 86400)}
        }
        sort_ = [("last_time_crawl_identity", 1)]
        limit_ = 10
        selected_fields_ = [
            '_id',
            'hiip_user_type', 'fb_user_type', 'fb_permission',
            'user_id', 'page_id', 'username', 'app_id']

        return Query(filter_=filter_, sort_=sort_, limit_=limit_, selected_fields_=selected_fields_, priority=1)

    @staticmethod
    def get_new_report_query(service_config: dict):
        filter_ = {
            'country_code': {'$in': service_config['MARKET']},
            'status': 'Created',
            'tracking_status': {'$nin': ['Missing', 'Tracking', 'Done']},
            'post_id': {'$exists': False}
        }
        sort_ = [("taken_at_timestamp", 1)]
        limit_ = 10
        selected_fields_ = ['_id', 'username', 'report_type', 'user_id', 'user_app_id', 'country_code',
                            'post_time_from', 'post_time_to', 'post_content', 'hiip_post_id', 'post_id']

        return Query(filter_=filter_, sort_=sort_, limit_=limit_, selected_fields_=selected_fields_, priority=1)

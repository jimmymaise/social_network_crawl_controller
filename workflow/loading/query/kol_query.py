import time

from workflow.loading.query.base_query import Query


class KOLQuery:
    @staticmethod
    def get_identity_query():
        filter_ = {
            'crawl_identity_status': {'$nin': ['Failed']},
            'hiip_user_type': {'$in': ['user', 'page']},
            'country_code': {'$elemMatch': {'$in': ['vi']}},
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

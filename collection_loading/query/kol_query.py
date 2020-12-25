import time

from .base_query import Query


class KOLQuery(Query):
    @staticmethod
    def get_identity_query():
        _filter = {
            'crawl_identity_status': {'$nin': ['Failed']},
            'hiip_user_type': {'$in': ['user', 'page']},
            'country_code': {'$elemMatch': {'$in': ['vi']}},
            '$or': [{'influencer_type': {'$nin': ['INFLUENCE_TYPE_IGNORE']}},
                    {'influencer_type': {'$exists': False}}],
            'last_time_crawl_identity': {'$lte': (time.time() - 86400)}
        }
        _sort = [("last_time_crawl_identity", 1)]
        _limit = 10
        selected_fields = [
            '_id',
            'hiip_user_type', 'fb_user_type', 'fb_permission',
            'user_id', 'page_id', 'username', 'app_id']

        return Query(_filter=_filter, _sort=_sort, _limit=_limit, selected_fields=selected_fields, priority=1)

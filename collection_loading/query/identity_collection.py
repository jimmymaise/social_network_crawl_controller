import time

from .base_query import Query


class IdentityQuery(Query):

    def __init__(self):
        self._filter = {
            'crawl_identity_status': {'$nin': ['Failed']},
            'hiip_user_type': {'$in': ['user', 'page']},
            'country_code': {'$elemMatch': {'$in': ['vi']}},
            '$or': [{'influencer_type': {'$nin': ['INFLUENCE_TYPE_IGNORE']}},
                    {'influencer_type': {'$exists': False}}],
            'last_time_crawl_identity': {'$lte': (time.time() - 86400)}
        }
        self._sort = [("last_time_crawl_post", 1)]
        self.selected_fields = [
            '_id',
            'hiip_user_type', 'fb_user_type', 'fb_permission',
            'user_id', 'page_id', 'username', 'app_id']

    def query_function(self):
        pass

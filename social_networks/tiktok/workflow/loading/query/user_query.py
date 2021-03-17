from core.workflows.loading.query.base_query import Query


class UserQuery:
    @staticmethod
    def get_sec_uid_from_username(list_username):
        filter_ = {
            'username': {'$in': list_username}
        }
        selected_fields = ['username', 'sec_uid', 'num_follower']
        return Query(filter_=filter_, selected_fields=selected_fields, priority=1, limit=None, sort_=None)

    @staticmethod
    def get_user_from_user_ids(user_ids, selected_fields=None):
        filter_ = {
            '_id': {'$in': user_ids}
        }
        return Query(filter_=filter_, selected_fields=selected_fields, priority=1, limit=None, sort_=None)

from core.workflows.loading.query.base_query import Query


class UserQuery:
    @staticmethod
    def get_sec_uid_from_username(listUsername):
        filter_ = {
            'username': {'$in': listUsername}
        }
        selected_fields = ['username', 'sec_uid']
        return Query(filter_=filter_, selected_fields=selected_fields, priority=1, limit=None, sort_=None)

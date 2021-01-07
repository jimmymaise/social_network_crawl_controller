from workflow.loading.query.base_query import Query


class ReportQuery:
    @staticmethod
    def get_report_service_query(service_config: dict):
        filter_ = {
            'country_code': {'$in': service_config['MARKET']},
            'status': 'Created',
            'tracking_status': {'$nin': ['Missing', 'Tracking', 'Done']},
            'post_id': {'$exists': False}
        }
        sort_ = [("taken_at_timestamp", 1)]
        limit_ = 10
        selected_fields = ['_id', 'username', 'report_type', 'user_id', 'user_app_id', 'country_code',
                           'post_time_from', 'post_time_to', 'post_content', 'hiip_post_id', 'post_id', 'post_link']

        return Query(filter_=filter_, sort_=sort_, limit_=limit_, selected_fields=selected_fields, priority=1)

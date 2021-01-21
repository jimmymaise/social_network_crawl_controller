from workflow.loading.query.base_query import Query


class ReportQuery:
    @staticmethod
    def get_reports_for_search_report_service(service_config: dict):
        filter_ = {
            'country_code': {'$in': service_config.get('MARKET')},
            f'{service_config["service_name"]}_status.status': {'$nin': ['success']},
        }
        filter_.pop('country_code') if not service_config.get('MARKET') else None
        sort_ = [("search_report_status.latest_update_time", 1)]
        limit = 10
        return Query(filter_=filter_, sort_=sort_, limit=limit, selected_fields=[], priority=1)

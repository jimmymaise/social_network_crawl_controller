from services.search_report_service import SearchReportService


class ServiceFactory:
    @staticmethod
    def create_service(service_name, service_config) -> SearchReportService:
        if service_name.upper() == 'SEARCH_REPORT':
            return SearchReportService(service_config)

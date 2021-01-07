from services.post_report_service import PostReportService


class ServiceFactory:
    @staticmethod
    def create_service(service_name, service_config) -> PostReportService:
        if service_name.upper() == 'POST_REPORT':
            return PostReportService(service_config)

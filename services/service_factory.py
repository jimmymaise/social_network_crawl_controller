from core.utils.constant import Constant
from services.search_report_service import SearchReportService


class ServiceFactory:
    @staticmethod
    def create_service(service_name, service_config) -> SearchReportService:
        if service_name.upper() == Constant.SERVICE_NAME_SEARCH_REPORT.upper():
            return SearchReportService(service_config)

from core.utils.constant import Constant
from services.search_report_service import SearchReportService
from services.comment_report_service import CommentReportService
from services.base_collection_service import CollectionService


class ServiceFactory:
    @staticmethod
    def create_service(service_name, service_config) -> CollectionService:
        if service_name.upper() == Constant.SERVICE_NAME_SEARCH_REPORT.upper():
            return SearchReportService(service_config)

        if service_name.upper() == Constant.SERVICE_NAME_COMMENT_REPORT.upper():
            return CommentReportService(service_config)

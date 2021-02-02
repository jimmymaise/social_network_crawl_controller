from social_networks.facebook.utils.constant import Constant
from core.services.base_collection_service import CollectionService
from social_networks.facebook.services.comment_report_service import CommentReportService
from social_networks.facebook.services.search_report_service import SearchReportService


class ServiceFactory:
    @staticmethod
    def create_service(service_name, service_config) -> CollectionService:
        if service_name.upper() == Constant.SERVICE_NAME_SEARCH_REPORT.upper():
            return SearchReportService(service_config)

        if service_name.upper() == Constant.SERVICE_NAME_COMMENT_REPORT.upper():
            return CommentReportService(service_config)

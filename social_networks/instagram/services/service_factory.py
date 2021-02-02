from enum import Enum

from core.services.base_collection_service import CollectionService
from social_networks.instagram.services.comment_report_service import CommentReportService
from social_networks.instagram.services.search_report_service import SearchReportService


class ServiceEnum(Enum):
    search_report = SearchReportService
    comment_report = CommentReportService


class ServiceFactory:
    @staticmethod
    def create_service(service_name, service_config) -> CollectionService:
        service_class = getattr(ServiceEnum, service_name.lower()).value
        return service_class(service_config)

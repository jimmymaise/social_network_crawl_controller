from enum import Enum

from core.services.base_collection_service import CollectionService
from social_networks.tiktok.services.user_collection_service import UserCollectionService
from social_networks.tiktok.services.posts_collection_service import PostsCollectionService
from social_networks.tiktok.services.posts_engagement_analytics_collection_service import PostsEngagementAnalyticsCollectionService


class ServiceEnum(Enum):
    user_collection = UserCollectionService
    posts_collection = PostsCollectionService
    posts_engagement_analytics_collection = PostsEngagementAnalyticsCollectionService


class ServiceFactory:
    @staticmethod
    def create_service(service_name, service_config) -> CollectionService:
        service_class = getattr(ServiceEnum, service_name.lower()).value
        return service_class(service_config)

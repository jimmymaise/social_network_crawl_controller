from enum import Enum

from core.services.base_collection_service import CollectionService
from social_networks.tiktok.services.user_collection_service import UserCollectionService
from social_networks.tiktok.services.posts_collection_service import PostsCollectionService


class ServiceEnum(Enum):
    user_collection = UserCollectionService
    posts_collection = PostsCollectionService


class ServiceFactory:
    @staticmethod
    def create_service(service_name, service_config) -> CollectionService:
        service_class = getattr(ServiceEnum, service_name.lower()).value
        return service_class(service_config)

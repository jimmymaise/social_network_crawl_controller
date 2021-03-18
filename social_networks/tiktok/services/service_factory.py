from enum import Enum

from core.services.base_collection_service import CollectionService
from social_networks.tiktok.services.user_collection_service import UserCollectionService
from social_networks.tiktok.services.post_list_collection_service import PostListCollectionService


class ServiceEnum(Enum):
    user_collection = UserCollectionService
    post_list_collection = PostListCollectionService


class ServiceFactory:
    @staticmethod
    def create_service(service_name, service_config, on_demand_handler=None) -> CollectionService:
        service_class = getattr(ServiceEnum, service_name.lower()).value
        return service_class(service_config, on_demand_handler)

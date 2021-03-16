from core.services.base_collection_service import CollectionService
from social_networks.tiktok.handlers.db_handler.kol_db_handler import KOLDBHandler
from social_networks.tiktok.handlers.db_handler.post_db_handler import PostDBHandler
from social_networks.tiktok.handlers.db_handler.user_db_handler import UserDBHandler
from social_networks.tiktok.utils.constant import Constant
from social_networks.tiktok.workflow.loading.load.report_load_handler import ReportLoadHandler
from social_networks.tiktok.workflow.loading.load.user_load_handler import UserLoadHandler
from social_networks.tiktok.workflow.loading.query.kol_query import KOLQuery
from social_networks.tiktok.workflow.loading.query.post_query import PostAggregate
from social_networks.tiktok.workflow.loading.query.user_query import UserQuery
from social_networks.tiktok.workflow.transform.posts_engagement_analytics_collection_transform_handler import \
    PostsEngagementAnalyticsCollectionTransformHandler


class PostsEngagementAnalyticsCollectionService(CollectionService):
    def __init__(self, service_config):
        super().__init__(service_config, Constant.COLLECTION_NAME_POST,
                         service_name=Constant.SERVICE_NAME_POSTS_COLLECTION)

    def _load_items(self) -> list:
        kol_db_handler = KOLDBHandler(self.db_connection)
        user_db_handler = UserDBHandler(self.db_connection)
        loader = ReportLoadHandler(kol_db_handler)
        query = KOLQuery.get_kols_for_engagement_collection_service(self.service_config)

        loader.add_query(query)
        load_items = loader.load_items()

        user_ids = [_['user_id'] for _ in load_items]

        query_user = UserQuery.get_user_from_user_ids(user_ids, selected_fields=['num_follower', '_id'])
        user_loader = UserLoadHandler(user_db_handler)
        user_loader.add_query(query_user)
        users = user_loader.load_items()
        return users

    def _collect_data(self, loaded_item):
        kol_db_handler = PostDBHandler(self.db_connection)
        loader = ReportLoadHandler(kol_db_handler)
        query = PostAggregate.get_post_statistics(loaded_item['_id'])

        load_items = loader.aggregate(query)
        return [{**loaded_item, **_} for _ in list(load_items)]

    def _transform_data(self, loaded_items, collected_data):
        transform = PostsEngagementAnalyticsCollectionTransformHandler(service_name=self.service_name)
        transformed_data = transform.process_item(loaded_items, collected_data)
        return transformed_data

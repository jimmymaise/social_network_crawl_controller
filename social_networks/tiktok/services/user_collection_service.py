from core.services.base_collection_service import CollectionService
from social_networks.tiktok.handlers.db_handler.kol_db_handler import KOLDBHandler
from social_networks.tiktok.handlers.queue_handler.message_schemas.user_message_schema import ReceivingUserMessageSchema
from social_networks.tiktok.utils.constant import Constant
from social_networks.tiktok.workflow.collect.api_collect_handler import APICollectHandler
from social_networks.tiktok.workflow.loading.load.report_load_handler import ReportLoadHandler
from social_networks.tiktok.workflow.loading.query.kol_query import KOLQuery
from social_networks.tiktok.workflow.transform.user_collection_transform_handler import UserCollectionTransformHandler


class UserCollectionService(CollectionService):
    def __init__(self, service_config, on_demand_handler=None):
        super().__init__(service_config, Constant.COLLECTION_NAME_KOL,
                         service_name=Constant.SERVICE_NAME_USER_COLLECTION, on_demand_handler=on_demand_handler)
        self.receive_message_schema = ReceivingUserMessageSchema
        self.message_mapping = {
            'hiip_user_id': 'hiip_user_id',
            'country_code': 'country_code',
            'user_id': 'social_id',
            'app_id': 'social_app_id',
            'username': 'social_user_name',
            '_id': 'hiip_user_id'
        }

    def _load_items_from_db(self) -> list:
        kol_db_handler = KOLDBHandler(self.db_connection)
        loader = ReportLoadHandler(kol_db_handler)
        query = KOLQuery.get_kols_for_user_collection_service(self.service_config)

        loader.add_query(query)
        load_items = loader.load_items()
        return load_items

    def _collect_data(self, loaded_item):
        # Currently we don't need to have tiktok account for crawling user collection
        collect_handler = APICollectHandler(crawl_account_handler=None)
        api_response = collect_handler.get_user_detail_from_lambda(
            lambda_base_url=self.system_config.LAMBDA_BASE_URL,
            username=loaded_item['username'],
            api_key=self.system_config.LAMBDA_X_API_KEY)
        collected_data = api_response['data']
        return collected_data

    def _transform_data(self, loaded_items, collected_data):
        user_collection_transform = UserCollectionTransformHandler(service_name=self.service_name)
        transformed_data = user_collection_transform.process_item(loaded_items, collected_data)
        return transformed_data

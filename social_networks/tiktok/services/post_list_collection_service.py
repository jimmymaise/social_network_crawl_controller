from core.handlers.crawl_account_handler import CrawlAccountHandler
from core.services.base_collection_service import CollectionService
from social_networks.tiktok.handlers.db_handler.kol_db_handler import KOLDBHandler
from social_networks.tiktok.handlers.db_handler.user_db_handler import UserDBHandler
from social_networks.tiktok.handlers.queue_handler.message_schemas.post_list_message_schema import PostListMessageSchema
from social_networks.tiktok.utils.constant import Constant
from social_networks.tiktok.workflow.collect.api_collect_handler import APICollectHandler
from social_networks.tiktok.workflow.loading.load.report_load_handler import ReportLoadHandler
from social_networks.tiktok.workflow.loading.load.user_load_handler import UserLoadHandler
from social_networks.tiktok.workflow.loading.query.kol_query import KOLQuery
from social_networks.tiktok.workflow.loading.query.user_query import UserQuery
from social_networks.tiktok.workflow.sync_data.sync_data_handler import SyncDataHandler
from social_networks.tiktok.workflow.transform.posts_collection_transform_handler import PostsCollectionTransformHandler


class PostListCollectionService(CollectionService):
    def __init__(self, service_config, on_demand_handler=None):
        super().__init__(service_config, Constant.COLLECTION_NAME_POST,
                         service_name=Constant.SERVICE_NAME_POSTS_COLLECTION, on_demand_handler=on_demand_handler)
        self.receive_message_schema = PostListMessageSchema
        self.loaded_item_message_mapping = {
            'country_code': 'country_code',
            'user_id': 'social_id',
            'app_id': 'social_app_id',
            'username': 'social_user_name',
            'sec_uid': 'sec_uid',
            '_id': 'hiip_user_id'
        }
        self.sync_data_handler = SyncDataHandler(self.db_connection)

    def _load_items_from_db(self) -> list:
        kol_db_handler = KOLDBHandler(self.db_connection)
        user_db_handler = UserDBHandler(self.db_connection)
        loader = ReportLoadHandler(kol_db_handler)
        query = KOLQuery.get_kols_for_posts_collection_service(self.service_config)

        loader.add_query(query)
        load_items = loader.load_items()

        usernames = [_['username'] for _ in load_items]

        query_sec_uid = UserQuery.get_sec_uid_from_username(usernames)
        user_loader = UserLoadHandler(user_db_handler)
        user_loader.add_query(query_sec_uid)
        sec_uids = user_loader.load_items()
        return sec_uids

    def _load_items_from_db_for_sqs(self, loaded_item) -> list:
        user_db_handler = UserDBHandler(self.db_connection)
        query_sec_uid = UserQuery.get_sec_uid_from_username([loaded_item['username']])
        user_loader = UserLoadHandler(user_db_handler)
        user_loader.add_query(query_sec_uid)
        sec_uids = user_loader.load_items()
        return sec_uids

    def _collect_data(self, loaded_item):
        crawl_account_handler = CrawlAccountHandler(account_base_url=self.system_config.AM_BASE_URL,
                                                    social_network=Constant.SOCIAL_NETWORK_TIKTOK,
                                                    service_name=self.service_name,
                                                    country=None)
        collect_handler = APICollectHandler(crawl_account_handler=crawl_account_handler)
        has_next_page = True
        next_cursor = None
        count = 0

        while has_next_page is True:
            self.logger.info(f'Next cursor {next_cursor}')
            response_body = collect_handler.get_user_posts_from_lambda(
                lambda_base_url=self.system_config.LAMBDA_BASE_URL,
                api_key=self.system_config.LAMBDA_X_API_KEY,
                sec_uid=loaded_item['sec_uid'],
                cursor=next_cursor,
                limit=Constant.POST_DEFAULT_PAGING_NUM_ITEM
            )

            has_next_page = response_body['paging']['has_next_page']
            next_cursor = response_body['paging']['next_cursor']
            for item in response_body['data']:
                yield item
                count += 1
                if count >= Constant.POST_MAX_LIST:
                    has_next_page = False
                    break

    def _transform_data(self, loaded_items, collected_data):
        posts_collection_transform = PostsCollectionTransformHandler(service_name=self.service_name)
        transformed_data = posts_collection_transform.process_item(loaded_items, collected_data)
        return transformed_data

    def _sync_data_to_sqs(self, loaded_item, transformed_data):
        username = loaded_item['username']

        self.sync_data_handler.user_data_sync(find_user_query={'username': username},
                                              queue_name=self.system_config.QUEUE_NAME_USER_DATA_SYNC)

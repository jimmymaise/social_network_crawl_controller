from workflow.collect.api_collect_handler import APICollectHandler
from core.handlers.crawl_account_handler import CrawlAccountHandler
from workflow.loading.load.kol_load_handler import KOLLoadHandler
from workflow.loading.query.kol_query import KOLQuery
from services.base_collection_service import CollectionService
from core.handlers.db_handler.kol_db_handler import KOLDBHandler
from workflow.transform.identity_item_transform_handler import IdentityItemTransformHandler


class PostService(CollectionService):
    def __init__(self):
        super().__init__()
        self.service_name = 'post_report'

    def _load_items(self) -> list:
        kol_db_handler = KOLDBHandler()
        loader = KOLLoadHandler(kol_db_handler)
        query = KOLQuery.get_new_report_query(self.service_config)

        loader.add_query(query)
        return loader.load_items()

    def _collect_data(self, loaded_item):
        # Play something with self.collect_handler to get data
        crawl_account_handler = CrawlAccountHandler(account_base_url=self.system_config['BASE_ACCOUNT_URL'],
                                                    social_network='facebook',
                                                    service_name=self.service_name,
                                                    country=None)
        collect_handler = APICollectHandler(crawl_account_handler=crawl_account_handler)
        collected_data = collect_handler.get_post_detail_data_from_lambda(
            lambda_base_url=self.system_config['BASE_LAMBDA_URL'], loaded_item=loaded_item)

        return collected_data

    def _transform_data(self, loaded_items, collected_data):
        # Play something with self.item_transform
        item_transform = IdentityItemTransformHandler()
        pass

    def _store_data(self, transformed_data):
        pass

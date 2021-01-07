from core.handlers.crawl_account_handler import CrawlAccountHandler
from core.handlers.db_handler.report_db_handler import ReportDB
from services.base_collection_service import CollectionService
from workflow.collect.api_collect_handler import APICollectHandler
from workflow.loading.load.report_load_handler import ReportLoadHandler
from workflow.loading.query.report_query import ReportQuery
from workflow.transform.identity_item_transform_handler import IdentityItemTransformHandler


class PostReportService(CollectionService):
    def __init__(self, service_config):
        super().__init__(service_config)
        self.service_name = 'post_report'

    def _load_items(self) -> list:
        mongodb_credential = {
            'db_username': self.system_config.MONGO_DB_HOST,
            'db_name': self.system_config.MONGO_DB_DATABASE_NAME,
            'db_password': self.system_config.MONGO_DB_PASSWORD,
            'db_host': self.system_config.MONGO_DB_HOST,
            'db_port': self.system_config.MONGO_DB_PORT
        }

        kol_db_handler = ReportDB(**mongodb_credential)
        loader = ReportLoadHandler(kol_db_handler)
        query = ReportQuery.get_report_service_query(self.service_config)

        loader.add_query(query)
        load_items = loader.load_items()
        return load_items

    def _collect_data(self, loaded_item):
        # Play something with self.collect_handler to get data
        crawl_account_handler = CrawlAccountHandler(account_base_url=self.system_config.AM_BASE_URL,
                                                    social_network='facebook',
                                                    service_name=self.service_name,
                                                    country=None)
        collect_handler = APICollectHandler(crawl_account_handler=crawl_account_handler)
        collected_data = collect_handler.get_post_detail_data_from_lambda(
            lambda_base_url=self.system_config.AM_BASE_URL, post_link=loaded_item['post_link'], api_key=
            self.system_config.LAMBDA_X_API_KEY_POST_DETAIL
        )

        return collected_data

    def _transform_data(self, loaded_items, collected_data):
        # Play something with self.item_transform
        item_transform = IdentityItemTransformHandler()
        pass

    def _store_data(self, transformed_data):
        pass

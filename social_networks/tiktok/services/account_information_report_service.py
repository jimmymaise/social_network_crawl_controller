from core.handlers.crawl_account_handler import CrawlAccountHandler
from core.services.base_collection_service import CollectionService
from social_networks.tiktok.handlers.db_handler.kol_db_handler import KOLDBHandler
from social_networks.tiktok.utils.constant import Constant
from social_networks.tiktok.workflow.collect.api_collect_handler import APICollectHandler
from social_networks.tiktok.workflow.loading.load.report_load_handler import ReportLoadHandler
from social_networks.tiktok.workflow.loading.query.kol_query import KOLQuery
from social_networks.tiktok.workflow.transform.user_collection_transform_handler import AccountInformationReportTransformHandler


class AccountInformationReportService(CollectionService):
    def __init__(self, service_config):
        super().__init__(service_config, Constant.COLLECTION_NAME_REPORT,
                         service_name=Constant.SERVICE_NAME_USER_COLLECTION)

    def _load_items(self) -> list:
        kol_db_handler = KOLDBHandler(self.db_connection)
        loader = ReportLoadHandler(kol_db_handler)
        query = KOLQuery.get_reports_for_user_collection_service(self.service_config)

        loader.add_query(query)
        load_items = loader.load_items()
        return load_items

    def _collect_data(self, loaded_item):
        crawl_account_handler = CrawlAccountHandler(account_base_url=self.system_config.AM_BASE_URL,
                                                    social_network=Constant.SOCIAL_NETWORK_TIKTOK,
                                                    service_name=self.service_name,
                                                    country=None)
        collect_handler = APICollectHandler(crawl_account_handler=crawl_account_handler)
        api_response = collect_handler.get_account_information_from_lambda(
            lambda_base_url=self.system_config.LAMBDA_BASE_URL,
            username=loaded_item['username'],
            api_key=self.system_config.LAMBDA_X_API_KEY_POST_DETAIL)
        collected_data = api_response['data']
        return collected_data

    def _transform_data(self, loaded_items, collected_data):
        user_collection_transform = AccountInformationReportTransformHandler(service_name=self.service_name)
        transformed_data = user_collection_transform.process_item(loaded_items, collected_data)
        return transformed_data

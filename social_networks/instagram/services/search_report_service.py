from core.handlers.crawl_account_handler import CrawlAccountHandler
from core.services.base_collection_service import CollectionService
from social_networks.instagram.handlers.db_handler.report_db_handler import ReportDBHandler
from social_networks.instagram.utils.constant import Constant
from social_networks.instagram.workflow.collect.api_collect_handler import APICollectHandler
from social_networks.instagram.workflow.loading.load.report_load_handler import ReportLoadHandler
from social_networks.instagram.workflow.loading.query.report_query import ReportQuery
from social_networks.instagram.workflow.transform.search_report_transform_handler import SearchReportTransformHandler


class SearchReportService(CollectionService):
    def __init__(self, service_config):
        super().__init__(service_config, Constant.COLLECTION_NAME_REPORT, Constant.SERVICE_NAME_SEARCH_REPORT)
        self.service_name = service_config['service_name'] = Constant.SERVICE_NAME_SEARCH_REPORT

    def _load_items_from_db(self) -> list:
        report_db_handler = ReportDBHandler(self.db_connection)
        loader = ReportLoadHandler(report_db_handler)
        query = ReportQuery.get_reports_for_search_report_service(self.service_config)

        loader.add_query(query)
        load_items = loader.load_items()
        return load_items

    def _collect_data(self, loaded_item):
        crawl_account_handler = CrawlAccountHandler(account_base_url=self.system_config.AM_BASE_URL,
                                                    social_network=Constant.SOCIAL_NETWORK_INSTAGRAM,
                                                    service_name=self.service_name,
                                                    country=None)
        collect_handler = APICollectHandler(crawl_account_handler=crawl_account_handler)
        api_response = collect_handler.get_post_detail_data_from_lambda(
            lambda_base_url=self.system_config.LAMBDA_BASE_URL,
            post_link=loaded_item['post_link'],
            api_key=self.system_config.LAMBDA_X_API_KEY)
        collected_data = api_response['data']
        return collected_data

    def _transform_data(self, loaded_items, collected_data):
        search_report_transform = SearchReportTransformHandler(service_name=self.service_name)
        transformed_data = search_report_transform.process_item(loaded_items, collected_data)
        return transformed_data

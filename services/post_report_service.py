from core.handlers.crawl_account_handler import CrawlAccountHandler
from core.handlers.db_handler.report_db_handler import ReportDBHandler
from core.logger.logger_handler import Logger
from services.base_collection_service import CollectionService
from workflow.collect.api_collect_handler import APICollectHandler
from workflow.loading.load.report_load_handler import ReportLoadHandler
from workflow.loading.query.report_query import ReportQuery
from workflow.transform.post_report_transform_handler import PostReportTransformHandler


class PostReportService(CollectionService):
    def __init__(self, service_config):
        super().__init__(service_config)
        self.service_name = service_config['service_name'] = 'post_report'
        self.logger = Logger().init_logger(logger_name=self.service_name,
                                           remove_old_log=True, )

    def _load_items(self) -> list:
        report_db_handler = ReportDBHandler(self.db_connection)
        loader = ReportLoadHandler(report_db_handler)
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
            lambda_base_url=self.system_config.LAMBDA_BASE_URL, post_link=loaded_item['post_link'], api_key=
            self.system_config.LAMBDA_X_API_KEY_POST_DETAIL
        )

        return collected_data

    def _transform_data(self, loaded_items, collected_data):
        # Play something with self.item_transform
        post_report_transform = PostReportTransformHandler(service_name=self.service_name )
        transformed_data = post_report_transform.process_item(loaded_items, collected_data)
        return transformed_data

from core.handlers.crawl_account_handler import CrawlAccountHandler
from core.handlers.db_handler.media_db_handler import MediaDBHandler
from core.handlers.db_handler.report_db_handler import ReportDBHandler
from services.base_collection_service import CollectionService
from workflow.collect.api_collect_handler import APICollectHandler
from workflow.loading.load.report_load_handler import ReportLoadHandler
from workflow.loading.query.report_query import ReportQuery
from workflow.transform.post_report_transform_handler import PostReportTransformHandler


class PostReportService(CollectionService):
    def __init__(self, service_config):
        super().__init__(service_config)
        self.service_name = 'post_report'
        self.mongodb_credential = {
            'db_username': self.system_config.MONGO_DB_HOST,
            'db_name': self.system_config.MONGO_DB_DATABASE_NAME,
            'db_password': self.system_config.MONGO_DB_PASSWORD,
            'db_host': self.system_config.MONGO_DB_HOST,
            'db_port': self.system_config.MONGO_DB_PORT
        }

    def _load_items(self) -> list:
        report_db_handler = ReportDBHandler(**self.mongodb_credential)
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
        post_report_transform = PostReportTransformHandler()
        transformed_data = post_report_transform.process_item(loaded_items, collected_data)
        return transformed_data

    def _store_data(self, transformed_data):
        db_report_handler = ReportDBHandler(**self.mongodb_credential)
        db_report_handler.bulk_write_many_update_objects(
            transformed_data.get('report_stored_objects')
        )

        db_post_handler = MediaDBHandler(**self.mongodb_credential)
        db_post_handler.bulk_write_many_update_objects(
            transformed_data.get('post_stored_objects'))

        db_user_handler = MediaDBHandler(**self.mongodb_credential)
        db_user_handler.bulk_write_many_update_objects(
            transformed_data.get('user_stored_objects'))

        db_kol_handler = MediaDBHandler(**self.mongodb_credential)
        db_kol_handler.bulk_write_many_update_objects(
            transformed_data.get('kol_stored_objects'))

        db_media_handler = MediaDBHandler(**self.mongodb_credential)
        db_media_handler.bulk_write_many_update_objects(
            transformed_data.get('media_stored_objects'))

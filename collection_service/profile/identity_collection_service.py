import time

from api_handler.lambda_api_handler import LambdaApiRequestHandler
from collect_handler.api_collect_handler import APICollectHandler
from collection_loading.load.kol_load_handler import KOLLoadHandler
from collection_loading.query.kol_query import KOLQuery
from collection_service.base_collection_service import CollectionService
from db_handler.kol_db_handler import KOLDBHandler
from item_transform.identity_item_transform_handler import IdentityItemTransformHandler


class IdentityService(CollectionService):
    def __init__(self, loader: KOLLoadHandler,
                 collect_handler: APICollectHandler,
                 item_transform: IdentityItemTransformHandler,
                 system_config: dict,
                 service_config: dict):
        super().__init__(loader, collect_handler, item_transform)
        self.service_name = 'identity'
        self.system_config = system_config
        self.service_config = service_config

    def _load_items(self) -> list:
        query = KOLQuery.get_identity_query()

        self.loader.add_query(query)
        return self.loader.load_items()

    def _get_crawl_data(self, loaded_items) -> list:
        # Play something with self.collect_handler to get data
        crawl_items = []

        for item in loaded_items:
            crawl_items.append(self.collect_handler.crawl_post_detail_data(item))
            # todo sleep time
        return crawl_items

    def _prepare_data_for_storing(self, loaded_items, crawled_items):
        # Play something with self.item_transform
        pass

    def _store_to_database(self, data):
        pass


class IdentityServiceRunner:

    def __init__(self, system_config, service_config):
        self.system_config = system_config
        self.service_config = service_config

        self.kol_db_handler = KOLDBHandler()
        self.loader = KOLLoadHandler(self.kol_db_handler)
        self.api_handler = LambdaApiRequestHandler(base_url=system_config['BASE_LAMBDA_URL'])
        self.collect_handler = APICollectHandler(self.api_handler, social_network='facebook', service='identity')
        self.item_transform = IdentityItemTransformHandler()

        self.identity_service = IdentityService(loader=self.loader,
                                                collect_handler=self.collect_handler,
                                                item_transform=self.item_transform,
                                                system_config=self.system_config,
                                                service_config=self.service_config,
                                                )

    def start(self):
        self.identity_service.process()

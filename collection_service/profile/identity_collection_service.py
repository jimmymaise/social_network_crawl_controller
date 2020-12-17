import time

from api_handler.lambda_api_handler import LambdaApiRequestHandler
from collect_handler.api_collect_handler import APICollectHandler
from collection_loading.load.kol_load_handler import KOLLoadHandler
from collection_loading.query.base_query import Query
from collection_service.base_collection_service import CollectionService
from database.db_handler import MongodbHandler
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
        # Play something with self.loads to get data
        _filter = {
            'crawl_identity_status': {'$nin': ['Failed']},
            'hiip_user_type': {'$in': ['user', 'page']},
            'country_code': {'$elemMatch': {'$in': ['vi']}},
            '$or': [{'influencer_type': {'$nin': self.service_config['INFLUENCE_TYPE_IGNORE']}},
                    {'influencer_type': {'$exists': False}}],
            'last_time_crawl_identity': {'$lte': (time.time() - 86400)}
        }
        _sort = [("last_time_crawl_post", 1)]
        selected_fields = [
            '_id',
            'hiip_user_type', 'fb_user_type', 'fb_permission',
            'user_id', 'page_id', 'username', 'app_id']

        query = Query(_filter=_filter, _sort=_sort, selected_fields=selected_fields,
                      _limit=self.service_config['LIMIT'], priority=1)

        self.loader.add_filter(query)
        return self.loader.load_items()

    def _get_crawl_data(self, loaded_items) -> list:
        # Play something with self.collect_handler to get data
        crawl_items = []

        for item in loaded_items:
            post_id = item.get('post_id')
            crawl_items.append(self.collect_handler.crawl_post_detail_data(post_id))
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

        self.db_handler = MongodbHandler(connection_uri=system_config['DB_URI'], database_name=system_config['DB_NAME'])
        self.loader = KOLLoadHandler(db_handler=self.db_handler)
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

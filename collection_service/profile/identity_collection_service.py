from collect_handler.api_collect_handler import APICollectHandler
from collection_loading.load.kol_load_handler import KOLLoadHandler
from collection_loading.query.kol_query import KOLQuery
from collection_service.base_collection_service import CollectionService
from db_handler.kol_db_handler import KOLDBHandler
from item_transform.identity_item_transform_handler import IdentityItemTransformHandler


class IdentityService(CollectionService):
    def __init__(self,
                 system_config: dict,
                 service_config: dict):
        super().__init__()
        self.service_name = 'identity'
        self.system_config = system_config
        self.service_config = service_config

    def _load_items(self) -> list:
        kol_db_handler = KOLDBHandler()
        loader = KOLLoadHandler(kol_db_handler)
        query = KOLQuery.get_identity_query()

        loader.add_query(query)
        return loader.load_items()

    def _get_collected_data(self, loaded_item):
        # Play something with self.collect_handler to get data
        collect_handler = APICollectHandler(base_url=self.system_config['BASE_LAMBDA_URL'],
                                            social_network='facebook',
                                            service=self.service_name)
        collected_data = collect_handler.get_post_detail_data_from_lambda(loaded_item)
        return collected_data

    def _prepare_data_for_storing(self, loaded_items, crawled_items):
        # Play something with self.item_transform
        item_transform = IdentityItemTransformHandler()
        pass

    def _store_to_database(self, data):
        pass

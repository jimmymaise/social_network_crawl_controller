from abc import abstractmethod

from core.logger.logger_handler import Logger


class BaseItemTransformHandler(object):
    @abstractmethod
    def __init__(self):
        self.logger = Logger.get_logger()

    @abstractmethod
    def process_item(self, loaded_item, collected_data):
        pass

    @staticmethod
    def _validate_schema(data, schema):
        error = {}
        try:
            schema().load(data)
        except Exception as e:
            error = e
        return data, error

    @staticmethod
    def _make_updated_object(filter_, stored_object, upsert=True):
        return {
            'filter': filter_,
            'update': stored_object,
            'upsert': upsert,

        }

    @staticmethod
    def _make_transformed_item(collection_name: str, updated_object_list: list):
        return {
            'collection_name': collection_name,
            'items': updated_object_list
        }

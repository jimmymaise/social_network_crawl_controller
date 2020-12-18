from abc import ABCMeta, abstractmethod


class BaseItemTransformHandler(object, ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def process_item(self, load_items, crawl_items):
        pass

    @abstractmethod
    def parser_user_objects(self):
        pass

    def _validate_schema(self, data, schema):
        error = {}
        try:
            schema().load(data)
        except Exception as e:
            error = e
        return data, error



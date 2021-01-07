from abc import ABCMeta, abstractmethod


class BaseItemTransformHandler(object):
    @abstractmethod
    def __init__(self):
        pass

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

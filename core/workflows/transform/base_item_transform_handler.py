import datetime
from abc import abstractmethod

from core.logger.logger_handler import Logger


class BaseItemTransformHandler:
    @abstractmethod
    def __init__(self, service_name):
        self.logger = Logger.get_logger()
        self.service_name = service_name
        self.now = datetime.datetime.now()

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
    def _make_transformed_item(*, updated_object_list: list = None, collection_name: str = None):
        return {
            'collection_name': collection_name,
            'items': updated_object_list
        }

    def _build_report_statuses_object(self):
        report_statuses_object = {
            f'{self.service_name}_status': {'status': 'success',
                                            'latest_updated_time': int(self.now.timestamp())
                                            },
            'response_server.is_update_report': True,
            'response_server.num_update': 0,
        }
        return report_statuses_object

    def _build_kol_statuses_object(self):
        report_statuses_object = {
            f'{self.service_name}_status': {'status': 'success',
                                            'latest_updated_time': int(self.now.timestamp())
                                            },
            'response_server.num_update': 0,
        }
        return report_statuses_object

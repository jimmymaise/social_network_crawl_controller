import json
from abc import ABCMeta, abstractmethod
import requests
from core.handlers.api_handler.api_specs.base_api_specs import BaseAPISpecs


class BaseApiRequestHandler(object, metaclass=ABCMeta):
    def __init__(self, base_url):
        self.base_url = base_url

    @abstractmethod
    def _handle_failed_request(self, response):
        pass

    @abstractmethod
    def _handle_success_request(self, response):
        pass

    @abstractmethod
    def _is_request_success(self, response):
        pass

    @staticmethod
    def _validate_schema(data, schema):
        error = {}
        try:
            schema().load(data)
        except Exception as e:
            error = e
        return data, error

    def _process_request(self, request_data: BaseAPISpecs):
        response = getattr(requests, request_data.method)(url=f'{self.base_url}/{request_data.path}',
                                                          header=request_data.header,
                                                          json=request_data.body)
        return json.loads(response.content, encoding='utf8')

    def call_api(self, request_data: BaseAPISpecs):
        is_valid_schema = True
        data, errors = self._validate_schema(request_data.body, request_data.request_schema)

        if errors:
            raise Exception('Invalid request data')

        response = self._process_request(request_data)
        if not self._is_request_success(response):
            self._handle_failed_request(response)
            return response

        self._handle_success_request(response)
        data, errors = self._validate_schema(response['collected_data'], request_data.response_schema)
        if errors:
            is_valid_schema = False
        return response, is_valid_schema
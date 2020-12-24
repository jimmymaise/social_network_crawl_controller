import json
import requests
from abc import abstractmethod


class BaseApiSpecs:
    base_url: str
    method: str
    path: str
    header: dict
    body: dict
    request_schema: object
    response_schema: object

    def __init__(self, base_url, method, path, header,
                 body, request_schema, response_schema):
        self.base_url = base_url
        self.method = method
        self.path = path
        self.header = header
        self.body = body
        self.request_schema = request_schema
        self.response_schema = response_schema

    def process_request(self):
        response = getattr(requests, self.method)(url=f'{self.base_url}/{self.path}',
                                                  header=self.header,
                                                  json=self.body)
        return json.loads(response.content, encoding='utf8')

    def call_api(self):
        is_valid_schema = True
        data, errors = self._validate_schema(self.body, self.request_schema)

        if errors:
            raise Exception('Invalid request data')

        response = self.process_request()
        if not self._is_request_success(response):
            self._handle_failed_request(response)
            return response

        self._handle_success_request(response)
        data, errors = self._validate_schema(response['collected_data'], self.response_schema)
        if errors:
            is_valid_schema = False
        return response, is_valid_schema

    def set_base_url(self, _url):
        self.base_url = _url

    def set_method(self, _method):
        self.method = _method

    def set_path(self, _path):
        self.path = _path

    def set_header(self, _header):
        self.header = _header

    def set_body(self, _body):
        self.body = _body

    def set_request_schema(self, _request_schema):
        self.request_schema = _request_schema

    def set_response_schema(self, _response_schema):
        self.response_schema = _response_schema

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

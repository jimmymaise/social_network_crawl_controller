from abc import abstractmethod


class BaseAPISpecs:
    method: str
    path: str
    header: dict
    body: dict
    request_schema: object
    response_schema: object

    def __init__(self, method, path, header, body, request_schema, response_schema):
        self.method = method
        self.path = path
        self.body = body
        self.header = header
        self.request_schema = request_schema
        self.response_schema = response_schema

    @abstractmethod
    def set_body_from_load_data(self, loaded_item, account_info):
        pass

    @abstractmethod
    def set_header_from_api_key(self, api_key):
        self.header = {'X-API-KEY': api_key}

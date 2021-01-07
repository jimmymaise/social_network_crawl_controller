from abc import abstractmethod


class BaseAPISpecs:

    def __init__(self, method: str, path: str, headers: dict, body, request_schema: object,
                 response_data_schema: object, response_data_key: str = 'data'):
        self.method = method
        self.path = path
        self.body = body
        self.headers = headers
        self.response_data_key = response_data_key
        self.request_schema = request_schema
        self.response_data_schema = response_data_schema

    @abstractmethod
    def set_body(self, **kwargs):
        pass

    @abstractmethod
    def set_headers(self, **kwargs):
        pass

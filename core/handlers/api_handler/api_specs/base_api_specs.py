from abc import abstractmethod


class BaseAPISpecs:

    def __init__(self, method: str, path: str, headers: dict, body, request_schema: object,
                 response_schema: object):
        self.method = method
        self.path = path
        self.body = body
        self.headers = headers
        self.request_schema = request_schema
        self.response_schema = response_schema

    @abstractmethod
    def set_body(self, **kwargs):
        pass

    @abstractmethod
    def set_headers(self, **kwargs):
        pass

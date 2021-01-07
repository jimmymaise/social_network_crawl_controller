from core.handlers.api_handler.base_api_handler import BaseApiRequestHandler


class LambdaApiRequestHandler(BaseApiRequestHandler):
    def __init__(self, base_url):
        super().__init__(base_url=base_url)

    def _handle_failed_request(self, response, request_data=None):
        # Should implement this methods
        pass

    def _handle_success_request(self, response, request_data=None):
        # Should implement this methods
        pass

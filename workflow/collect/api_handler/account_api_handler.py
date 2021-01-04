from workflow.collect.api_handler.base_api_handler import BaseApiRequestHandler


class AccountAPIRequestHandler(BaseApiRequestHandler):
    def __init__(self, base_url):
        super().__init__(base_url=base_url)

    def _handle_failed_request(self, response):
        # Should implement this methods
        pass

    def _handle_success_request(self, response):
        # Should implement this methods
        pass

    def _is_request_success(self, response):
        # Should implement this methods
        return response.status_code in [200, 201]

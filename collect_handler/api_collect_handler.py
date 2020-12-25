from account_manager.account_manager_handler import AccountManager
from api_handler.api_specs.lambda_api_specs.post_detail_api_specs import APIPath
from api_handler.api_specs.lambda_api_specs.post_detail_api_specs import \
    PostDetailAPIResponseSchema, PostDetailAPIRequestSchema
from api_handler.api_specs.lambda_api_specs.post_detail_api_specs import PostDetailAPISpecs
from api_handler.lambda_api_handler import LambdaApiRequestHandler
from collect_handler.base_collect_handler import BaseCollectHandler


class APICollectHandler(BaseCollectHandler):
    def __init__(self, api_handler: LambdaApiRequestHandler, social_network, service, country=None):
        super().__init__()
        self.type = 'api'
        self.api_handler = api_handler
        self.social_network = social_network
        self.service = service
        self.country = country
        self.account_id = None
        self.account_info = None
        self.account_manager = AccountManager()

    def _get_account_id_token(self):
        self.account_id, self.account_info = self.account_manager.get_account_from_api(
            self.social_network, self.service, self.country
        )

    def _update_account_token(self, status_code, message):
        self.account_manager.update_account_status(
            social_network=self.social_network, account_id=self.account_id, status_code=status_code,
            message=message
        )

    def crawl_post_detail_data(self, **kwargs) -> dict:
        self._get_account_id_token()

        api_request_data = PostDetailAPISpecs()
        response, is_valid_schema = self.api_handler.call_api(
            request_data=api_request_data

        )
        self._update_account_token(response.status_code, 'Done')
        if is_valid_schema:
            return response['collect_data']

        return {}

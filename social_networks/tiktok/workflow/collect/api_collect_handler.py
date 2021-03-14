from core.handlers.api_handler.lambda_api_handler import LambdaApiRequestHandler
from core.handlers.crawl_account_handler import CrawlAccountHandler
from core.utils.exceptions import ErrorResponseFailed, ErrorResponseFormat
from core.workflows.collect.base_collect_handler import BaseCollectHandler
from social_networks.tiktok.handlers.api_handler.lambda_api_specs.user_detail_api_spec import \
    UserDetailAPISpecs
from social_networks.tiktok.handlers.api_handler.lambda_api_specs.user_posts_api_spec import UserPostsAPISpecs


class APICollectHandler(BaseCollectHandler):
    def __init__(self, crawl_account_handler: CrawlAccountHandler = None):
        super().__init__()
        self.crawl_account_handler = crawl_account_handler

    def get_user_detail_from_lambda(self, lambda_base_url, username, api_key) -> dict:

        account_info = self.crawl_account_handler and self.crawl_account_handler.get_account_id_token()

        lambda_api_handler = LambdaApiRequestHandler(base_url=lambda_base_url)

        post_detail_api_request_data = UserDetailAPISpecs()
        post_detail_api_request_data.set_body(username=username, account_info=account_info)
        post_detail_api_request_data.set_headers(api_key)

        response, success, schema_errors = lambda_api_handler.call_api(
            request_data=post_detail_api_request_data
        )

        if not success:
            raise ErrorResponseFailed(f'API Response: {response.text}')
        if schema_errors:
            raise ErrorResponseFormat(f'API Response Schema error: {schema_errors}')

        return response.json()

    def get_user_posts_from_lambda(self, lambda_base_url, sec_uid, cursor, api_key) -> dict:
        lambda_api_handler = LambdaApiRequestHandler(base_url=lambda_base_url)

        user_posts_api_request_data = UserPostsAPISpecs()
        user_posts_api_request_data.set_body(sec_uid=sec_uid, cursor=cursor)
        user_posts_api_request_data.set_headers(api_key)

        response, success, schema_errors = lambda_api_handler.call_api(
            request_data=user_posts_api_request_data
        )

        if not success:
            raise ErrorResponseFailed(f'API Response: {response.text}')
        if schema_errors:
            raise ErrorResponseFormat(f'API Response Schema error: {schema_errors}')

        return response.json()

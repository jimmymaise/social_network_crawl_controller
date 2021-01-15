from core.handlers.api_handler.api_specs.lambda_api_specs.post_detail_api_specs import PostDetailAPISpecs
from core.handlers.api_handler.lambda_api_handler import LambdaApiRequestHandler
from core.handlers.crawl_account_handler import CrawlAccountHandler
from core.utils.exceptions import ErrorResponseFailed, ErrorResponseFormat
from workflow.collect.base_collect_handler import BaseCollectHandler


class APICollectHandler(BaseCollectHandler):
    def __init__(self, crawl_account_handler: CrawlAccountHandler):
        super().__init__()
        self.type = 'api'
        self.crawl_account_handler = crawl_account_handler

    def get_post_detail_data_from_lambda(self, lambda_base_url, post_link, api_key) -> dict:
        account_info, account_id = self.crawl_account_handler.get_account_id_token()
        lambda_api_handler = LambdaApiRequestHandler(base_url=lambda_base_url)

        post_detail_api_request_data = PostDetailAPISpecs()
        post_detail_api_request_data.set_body(post_link=post_link, account_info=account_info)
        post_detail_api_request_data.set_headers(api_key)

        response, success, schema_errors = lambda_api_handler.call_api(
            request_data=post_detail_api_request_data
        )

        if not success:
            raise ErrorResponseFailed()
        if schema_errors:
            raise ErrorResponseFormat()

        return response.json()[post_detail_api_request_data.response_data_key]

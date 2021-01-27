from core.handlers.api_handler.api_specs.lambda_api_specs.post_detail_api_specs import PostDetailAPISpecs
from core.handlers.api_handler.lambda_api_handler import LambdaApiRequestHandler
from core.handlers.crawl_account_handler import CrawlAccountHandler
from core.utils.constant import Constant
from core.utils.exceptions import ErrorResponseFailed, ErrorResponseFormat, ErrorLinkFormat
from workflow.collect.base_collect_handler import BaseCollectHandler
from workflow.collect.utils.api_collect_utils import APICollectUtils


class APICollectHandler(BaseCollectHandler):
    def __init__(self, crawl_account_handler: CrawlAccountHandler):
        super().__init__()
        self.crawl_account_handler = crawl_account_handler

    def get_post_detail_data_from_lambda(self, lambda_base_url, post_link, api_key,
                                         social_type=Constant.SOCIAL_TYPE_PROFILE) -> dict:

        if not APICollectUtils.is_validate_post_link_format(post_link):
            raise ErrorLinkFormat(f'Post Link Error:{post_link}')

        account_info, account_id = self.crawl_account_handler.get_account_id_token()
        lambda_api_handler = LambdaApiRequestHandler(base_url=lambda_base_url)

        post_detail_api_request_data = PostDetailAPISpecs()
        post_detail_api_request_data.set_body(post_link=post_link, account_info=account_info, social_type=social_type)
        post_detail_api_request_data.set_headers(api_key)

        response, success, schema_errors = lambda_api_handler.call_api(
            request_data=post_detail_api_request_data
        )

        if not success:
            raise ErrorResponseFailed(f'API Response: {response.text}')
        if schema_errors:
            raise ErrorResponseFormat(f'API Response Schema error: {schema_errors}')

        return response.json()[post_detail_api_request_data.response_data_key]

    def get_comment_from_lambdas(self, lambda_base_url, post_link, api_key,
                                 social_type=Constant.SOCIAL_TYPE_PROFILE):
        pass

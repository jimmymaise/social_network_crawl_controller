from core.handlers.api_handler.api_specs.lambda_api_specs.post_detail_api_specs import PostDetailAPISpecs
from core.handlers.api_handler.lambda_api_handler import LambdaApiRequestHandler
from core.handlers.crawl_account_handler import CrawlAccountHandler
from workflow.collect.base_collect_handler import BaseCollectHandler


class APICollectHandler(BaseCollectHandler):
    def __init__(self, crawl_account_handler: CrawlAccountHandler):
        super().__init__()
        self.type = 'api'
        self.crawl_account_handler = crawl_account_handler

    def get_post_detail_data_from_lambda(self, lambda_base_url, loaded_item) -> dict:
        account_info, account_id = self.crawl_account_handler.get_account_id_token()

        lambda_api_handler = LambdaApiRequestHandler(base_url=lambda_base_url)
        api_request_data = PostDetailAPISpecs()
        api_request_data.set_body_from_load_data(loaded_item=loaded_item, account_info=account_info)

        response, is_valid_schema = lambda_api_handler.call_api(
            request_data=api_request_data
        )
        if account_id:
            self.crawl_account_handler.update_account_token(account_id=account_id, status_code=response.status_code,
                                                            message='Done')
        if is_valid_schema:
            return response['collected_data']


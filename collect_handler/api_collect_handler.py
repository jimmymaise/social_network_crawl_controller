import time
import traceback

import requests

from api_handler.account_api_handler import AccountAPIRequestHandler
from api_handler.api_specs.account_api_specs.account_get_specs import AccountGetSpecs
from api_handler.api_specs.account_api_specs.account_update_specs import AccountUpdateSpecs
from api_handler.api_specs.lambda_api_specs.post_detail_api_specs import PostDetailAPISpecs
from api_handler.lambda_api_handler import LambdaApiRequestHandler
from collect_handler.base_collect_handler import BaseCollectHandler
from config.account_config import AccountAPIConfig


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
        self.account_manager = AccountAPIRequestHandler('')

    def _get_account_id_token(self):
        account_spec = AccountGetSpecs()
        account_spec.set_body_for_account_get(self.social_network, self.service, self.country)

        num_request = 0
        while num_request < AccountAPIConfig.MAX_REQUEST_ACCOUNT:
            response_obj, is_valid_schema = self.api_handler.call_api(
                request_data=account_spec
            )
            print(response_obj.text)
            try:
                account_data = response_obj.json().get('data')
            except Exception as ex:
                print('Fail to get account data: ', ex)
                traceback.print_exc()
                continue

            if account_data:
                self.account_info = account_data['info']
                self.account_id = account_data['accountId']
                break
            time.sleep(AccountAPIConfig.DEFAULT_SLEEP_TIME)
            num_request += 1

    def _update_account_token(self, status_code, message):
        account_spec = AccountUpdateSpecs()
        account_spec.set_body_from_account_update(self.social_network, self.account_id, status_code, message)
        result = "Fail"

        response_obj, is_valid_schema = self.api_handler.call_api(
            request_data=account_spec
        )
        if response_obj.status_code == 200:
            response_code = None
            try:
                response_code = response_obj.json()['status_code']
            except Exception as ex:
                print("Fail to update account status, Details: ", ex)
            if response_code == 200:
                result = "Done"
        return result

    def crawl_post_detail_data(self, items_load) -> dict:
        self._get_account_id_token()

        api_request_data = PostDetailAPISpecs()
        api_request_data.set_body_from_load_data(item_load=items_load, account_info={})

        response, is_valid_schema = self.api_handler.call_api(
            request_data=api_request_data
        )
        self._update_account_token(response.status_code, 'Done')
        if is_valid_schema:
            return response['collect_data']

        return {}

import time
import traceback

from core.handlers.api_handler.account_api_handler import AccountAPIRequestHandler
from core.handlers.api_handler.api_specs.account_api_specs.account_get_specs import AccountGetSpecs
from core.handlers.api_handler.api_specs.account_api_specs.account_update_specs import AccountUpdateSpecs
from config.account_config import AccountAPIConfig


class CrawlAccountHandler:
    def __init__(self, account_base_url, social_network, service_name, country=None):
        super().__init__()
        self.type = 'api'
        self.social_network = social_network
        self.service_name = service_name
        self.country = country
        self.account_api = AccountAPIRequestHandler(account_base_url)

    def get_account_id_token(self):
        account_spec = AccountGetSpecs()
        account_spec.set_body_for_account_get(self.social_network, self.service_name, self.country)

        num_request = 0
        while num_request < AccountAPIConfig.MAX_REQUEST_ACCOUNT:
            response_obj, is_valid_schema = self.account_api.call_api(
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
                account_info = account_data['info']
                account_id = account_data['accountId']
                return account_info, account_id
            time.sleep(AccountAPIConfig.DEFAULT_SLEEP_TIME)
            num_request += 1

    def update_account_token(self, account_id, status_code, message):
        account_spec = AccountUpdateSpecs()
        account_spec.set_body_from_account_update(self.social_network, account_id, status_code, message)
        result = "Fail"

        response_obj, is_valid_schema = self.account_api.call_api(
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

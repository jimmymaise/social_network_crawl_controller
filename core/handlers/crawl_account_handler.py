import logging

from core.handlers.api_handler.account_api_handler import AccountAPIRequestHandler
from core.handlers.api_handler.api_specs.account_api_specs.account_get_specs import AccountGetSpecs
from core.handlers.api_handler.api_specs.account_api_specs.account_update_specs import AccountUpdateSpecs
from core.utils.constant import Constant


class CrawlAccountHandler:

    def __init__(self, account_base_url, social_network, service_name, country=None):
        super().__init__()
        self.social_network = social_network
        self.service_name = service_name
        self.country = country
        self.account_api = AccountAPIRequestHandler(account_base_url)
        self.account_spec = AccountGetSpecs()
        self.account_spec.set_body(self.social_network, self.service_name, self.country)
        self.logger = logging.getLogger()

    def get_account_id_token(self):
        response, success, schema_errors = self.account_api.call_api(
            request_data=self.account_spec,
            max_attempts=Constant.AM_MAX_REQUEST,
            retry_time_sleep=Constant.AM_DEFAULT_SLEEP_TIME
        )
        account_info, account_id = None, None
        if success and not schema_errors:
            account_data = response.json().get('data')
            account_info = account_data['info']
            account_id = account_data['accountId']
        return account_info, account_id

    def update_account_token(self, account_id, status_code, message):
        account_spec = AccountUpdateSpecs()
        account_spec.set_body(self.social_network, account_id, status_code, message)
        response_obj, is_valid_schema = self.account_api.call_api(
            request_data=account_spec
        )
        return is_valid_schema

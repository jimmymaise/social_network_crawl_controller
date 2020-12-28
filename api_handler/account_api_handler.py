import time
import traceback
from abc import ABC

import requests
from config.account_config import AccountAPIConfig
from api_handler.base_api_handler import BaseApiRequestHandler
from api_handler.api_specs.account_api_specs.account_get_specs import AccountGetSpecs
from api_handler.api_specs.account_api_specs.account_update_specs import AccountUpdateSpecs


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

    @staticmethod
    def get_account_from_api(social_network, service, country=None):
        account_id = None
        account_info = None
        account_spec = AccountGetSpecs()
        account_spec.set_body_for_account_get(social_network, service, country)
        payload = account_spec.get_payload()

        num_request = 0
        while num_request < AccountAPIConfig.MAX_REQUEST_ACCOUNT:
            response_obj = requests.post(url=AccountAPIConfig.AM_GET_ACCOUNT_URL, json=payload)
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
                break
            time.sleep(AccountAPIConfig.DEFAULT_SLEEP_TIME)
            num_request += 1
        return account_id, account_info

    @staticmethod
    def update_account_status(social_network, account_id, status_code, message=None):
        account_spec = AccountUpdateSpecs()
        account_spec.set_body_from_account_update(social_network, account_id, status_code, message)
        payload = account_spec.get_payload()
        result = "Fail"
        response_obj = requests.post(url=AccountAPIConfig.AM_UPDATE_STATUS, json=payload)
        if response_obj.status_code == 200:
            response_code = None
            try:
                response_code = response_obj.json()['status_code']
            except Exception as ex:
                print("Fail to update account status, Details: ", ex)
            if response_code == 200:
                result = "Done"
        return result

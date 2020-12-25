import time
import traceback
from abc import ABC

import requests
from config.account_config import AccountAPIConfig
from api_handler.base_api_handler import BaseApiRequestHandler
from api_handler.api_specs.account_api_specs.account_request_specs import AccountRequestSpecs
from api_handler.api_specs.account_api_specs.account_update_specs import AccountUpdateSpecs


class AccountAPIRequestHandler(BaseApiRequestHandler, ABC):

    @staticmethod
    def get_account_from_api(social_network, service, country=None):
        account_id = None
        account_info = None
        account_spec = AccountRequestSpecs()
        account_spec.set_api_body(social_network, service, country)
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
        account_spec.set_api_body(social_network, account_id, status_code, message)
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

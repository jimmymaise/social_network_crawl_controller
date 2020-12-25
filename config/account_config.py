import os


class AccountAPIConfig:
    AM_BASE_URL = os.getenv('AM_BASE_URL', 'http://34.219.102.184:9099')
    AM_GET_ACCOUNT_URL = f'{AM_BASE_URL}/request'
    AM_UPDATE_STATUS = f'{AM_BASE_URL}/update_status'
    MAX_REQUEST_ACCOUNT = 3
    DEFAULT_SLEEP_TIME = 30
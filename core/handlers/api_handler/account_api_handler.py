import json

import requests

from config.system_config import SystemConfig
from core.handlers.api_handler.base_api_handler import BaseApiRequestHandler
from core.utils.constant import Constant


class AccountAPIRequestHandler(BaseApiRequestHandler):
    def __init__(self, base_url):
        super().__init__(base_url=base_url)

    def _handle_failed_request(self, response, request_data=None):
        payload = {Constant.SLACK_DEFAULT_NOTIFICATION_FIELD: response.text}
        slack_webhook = SystemConfig.get_system_config().SLACK_NOTIFICATION_URL
        requests.post(slack_webhook, data=json.dumps(payload))

    def _handle_success_request(self, response, request_data=None):
        # Should implement this methods
        pass

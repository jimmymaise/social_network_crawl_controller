import json
from config.system_config import SystemConfig
import requests

from core.handlers.api_handler.base_api_handler import BaseApiRequestHandler


class AccountAPIRequestHandler(BaseApiRequestHandler):
    def __init__(self, base_url):
        super().__init__(base_url=base_url)

    def _handle_failed_request(self, response, request_data=None):
        payload = {'text': response.text}
        slack_webhook = SystemConfig.SLACK_NOTIFICATION_URL
        requests.post(slack_webhook, data=json.dumps(payload))

    def _handle_success_request(self, response, request_data=None):
        # Should implement this methods
        pass

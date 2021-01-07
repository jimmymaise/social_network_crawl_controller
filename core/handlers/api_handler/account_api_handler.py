import json

import requests

from core.handlers.api_handler.base_api_handler import BaseApiRequestHandler


class AccountAPIRequestHandler(BaseApiRequestHandler):
    def __init__(self, base_url):
        super().__init__(base_url=base_url)

    def _handle_failed_request(self, response, request_data=None):
        # todo: Should refactor this one. Just for demo purpose
        payload = {'response': response.text,
                   'url': response.url,
                   'request_body': json.loads(response.request.body, encoding='utf8')
                   }
        slack_webhook = 'https://hooks.slack.com/services/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'
        requests.post(slack_webhook, data=json.dumps(payload))

    def _handle_success_request(self, response, request_data=None):
        # Should implement this methods
        pass

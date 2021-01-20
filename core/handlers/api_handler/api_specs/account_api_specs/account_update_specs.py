from marshmallow import Schema, EXCLUDE

from core.handlers.api_handler.api_specs.base_api_specs import BaseAPISpecs
from core.utils.constant import Constant


class AccountUpdateSpecs(BaseAPISpecs):
    def __init__(self):
        super().__init__(method='post',
                         path=Constant.AM_API_UPDATE_CRAWL_ACCOUNT_PATH,
                         headers={},
                         body={},
                         request_schema=AccountUpdateAPIRequestSchema,
                         response_data_schema=AccountUpdateAPIResponseSchema)

    def set_headers(self, **kwargs):
        raise NotImplementedError()

    def set_body(self, social_network, account_id, status_code, message=None):
        _body = {
            "api_type": "UPDATE_STATUS",
            "api_body": {
                "social_network": social_network.upper(),
                "account_ID": account_id,
                "data": {
                    "status_code": status_code,
                    "message": message
                }
            }
        }
        self.body = _body


class AccountUpdateAPIResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class AccountUpdateAPIRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

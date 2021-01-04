from abc import ABC
from marshmallow import Schema, EXCLUDE
from core.handlers.api_handler.api_specs.base_api_specs import BaseAPISpecs


class AccountUpdateSpecs(BaseAPISpecs, ABC):
    def __init__(self):
        super().__init__(method='POST',
                         path='account_update',
                         header={},
                         body={},
                         request_schema=AccountUpdateAPIRequestSchema,
                         response_schema=AccountUpdateAPIResponseSchema)

    def set_body_from_account_update(self, social_network, account_id, status_code, message=None):
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

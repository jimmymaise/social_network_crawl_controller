from marshmallow import Schema, EXCLUDE, fields

from core.handlers.api_handler.api_specs.base_api_specs import BaseAPISpecs
from core.utils.constant import Constant


class AccountGetSpecs(BaseAPISpecs):
    def __init__(self):
        super().__init__(method='post',
                         path=Constant.AM_API_GET_CRAWL_ACCOUNT_PATH,
                         headers={},
                         body={},
                         request_schema=AccountGetAPIRequestSchema,
                         response_schema=AccountGetAPIResponseSchema)

    def set_headers(self, **kwargs):
        raise NotImplementedError()

    def set_body(self, social_network, service, country=None):
        _body = {
            "api_type": "GET",
            "api_body": {
                "social_network": social_network.upper() if isinstance(social_network, str) else "ALL",
                "service_name": service.upper() if isinstance(service, str) else "ALL",
                "country": country.upper() if isinstance(country, str) else "ALL",
            }
        }
        self.body = _body


class AccountGetAPIResponseDataItemSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    accountId = fields.Str()
    info = fields.Str()
    type = fields.Str()
    username = fields.Str()


class AccountGetAPIResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    data = fields.Nested(AccountGetAPIResponseDataItemSchema)


class AccountGetAPIRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    api_type = fields.Str()
    api_body = fields.Dict()

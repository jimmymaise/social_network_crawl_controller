from abc import ABC
from marshmallow import Schema, EXCLUDE
from workflow.collect.api_handler.api_specs.base_api_specs import BaseAPISpecs


class AccountGetSpecs(BaseAPISpecs, ABC):
    def __init__(self):
        super().__init__(method='POST',
                         path='account_get',
                         header={},
                         body={},
                         request_schema=AccountGetAPIRequestSchema,
                         response_schema=AccountGetAPIResponseSchema)

    def set_body_for_account_get(self, social_network, service, country=None):
        _body = {
            "api_type": "GET",
            "api_body": {
                "social_network": social_network.upper() if isinstance(social_network, str) else "ALL",
                "service_name": service.upper() if isinstance(service, str) else "ALL",
                "country": country.upper() if isinstance(country, str) else "ALL",
            }
        }
        self.body = _body


class AccountGetAPIResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class AccountGetAPIRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

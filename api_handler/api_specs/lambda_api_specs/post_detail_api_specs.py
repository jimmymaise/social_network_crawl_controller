from marshmallow import Schema, fields, EXCLUDE
from api_handler.api_specs.base_api_specs import BaseAPISpecs, BaseUserSchema, BasePostSchema
from config.env_config import LAMBDA_CONFIG


class PostDetailAPISpecs(BaseAPISpecs):
    def __init__(self):
        super().__init__(method='POST',
                         path='post_detail',
                         header={},
                         body={},
                         request_schema=PostDetailAPIRequestSchema,
                         response_schema=PostDetailAPIResponseSchema)

    def set_body_from_load_data(self, item_load: dict, account_info: dict):

        _body = {'post_link': item_load.get('post_link'),
                 'token': account_info.get('token')}

        self.body = _body

    def set_header_from_config_env(self):

        self.header = {'X-API-KEY': LAMBDA_CONFIG.get('X-API-KEY_POST_DETAIL')}


class PostDetailAPIResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user = fields.Nested(BaseUserSchema)
    post = fields.Nested(BasePostSchema)


class PostDetailAPIRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    pass

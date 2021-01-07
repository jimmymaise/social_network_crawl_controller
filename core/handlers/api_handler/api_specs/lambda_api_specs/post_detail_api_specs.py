from marshmallow import Schema, fields, EXCLUDE

from config.env_config import LAMBDA_CONFIG
from core.handlers.api_handler.api_specs.base_api_specs import BaseAPISpecs


class PostDetailAPISpecs(BaseAPISpecs):
    def __init__(self):
        super().__init__(method='POST',
                         path='post_detail',
                         header={},
                         body={},
                         request_schema=PostDetailAPIRequestSchema,
                         response_data_schema=PostDetailAPIResponseSchema)

        self.set_header(LAMBDA_CONFIG.get('X-API-KEY_POST_DETAIL'))

    def set_body(self, loaded_item: dict, account_info: dict):
        self.body = {'post_link': loaded_item.get('post_link'),
                     'token': account_info.get('token')}

    def set_header(self, api_key):
        self.header = {'X-API-KEY': api_key}


class BaseUserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    username = fields.Str()
    user_id = fields.Int()
    avatar = fields.Str()


class BasePostSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    content = fields.Str()
    full_picture = fields.Str()
    num_reaction = fields.Int()
    num_comment = fields.Int()
    num_share = fields.Int()
    view_count = fields.Int()
    feedback_id = fields.Str()


class BaseStatusSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    status_code = fields.Int()
    cookie_status = fields.Int()
    details = fields.Str()


class PostDetailAPIResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user = fields.Nested(BaseUserSchema)
    post = fields.Nested(BasePostSchema)


class PostDetailAPIRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    pass

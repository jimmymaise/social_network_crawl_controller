from marshmallow import Schema, fields, EXCLUDE

from core.handlers.api_handler.api_specs.base_api_specs import BaseAPISpecs
from social_networks.instagram.utils.constant import Constant


class PostDetailAPISpecs(BaseAPISpecs):
    def __init__(self):
        super().__init__(method='post',
                         path=Constant.LAMBDA_API_CRAWL_POST_DETAIL_PATH,
                         headers={},
                         body={},
                         request_schema=PostDetailAPIRequestSchema,
                         response_schema=PostDetailAPIResponseSchema)

    def set_body(self, post_link: str, account_info: dict, social_type=Constant.SOCIAL_TYPE_PROFILE):
        self.body = {'link': post_link,
                     'social_type': social_type,
                     'account_info': account_info
                     }

    def set_headers(self, api_key):
        self.headers = {'X-API-KEY': api_key}


class BaseUserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Int()
    username = fields.Str()
    avatar = fields.Str()


class BasePostSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    content = fields.Str(required=True)
    display_url = fields.Str()
    num_like = fields.Int(required=True)
    num_comment = fields.Int(required=True)
    view_count = fields.Int(required=True)
    taken_at_timestamp = fields.Int(required=True)

    shortcode = fields.Str(required=True)
    user_id = fields.Int(required=True)
    post_type = fields.Str(required=True)
    _id = fields.Int(required=True)


class BaseStatusSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    status_code = fields.Int()
    cookie_status = fields.Int()
    details = fields.Str()


class PostDetailAPIResponseDataItemSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user = fields.Nested(BaseUserSchema)
    post = fields.Nested(BasePostSchema, required=True)


class PostDetailAPIResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    data = fields.Nested(PostDetailAPIResponseDataItemSchema)


class PostDetailAPIRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    pass

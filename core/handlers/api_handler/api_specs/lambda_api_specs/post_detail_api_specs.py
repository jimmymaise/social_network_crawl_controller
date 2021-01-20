from marshmallow import Schema, fields, EXCLUDE

from core.handlers.api_handler.api_specs.base_api_specs import BaseAPISpecs
from core.utils.constant import Constant


class PostDetailAPISpecs(BaseAPISpecs):
    def __init__(self):
        super().__init__(method='post',
                         path=Constant.LAMBDA_API_CRAWL_POST_DETAIL_PATH,
                         headers={},
                         body={},
                         request_schema=PostDetailAPIRequestSchema,
                         response_data_schema=PostDetailAPIResponseSchema)

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

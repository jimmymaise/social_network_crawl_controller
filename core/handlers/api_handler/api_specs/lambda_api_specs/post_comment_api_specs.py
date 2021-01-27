from marshmallow import Schema, fields, EXCLUDE

from core.handlers.api_handler.api_specs.base_api_specs import BaseAPISpecs
from core.utils.constant import Constant


class PostCommentAPISpecs(BaseAPISpecs):
    def __init__(self):
        super().__init__(method='post',
                         path=Constant.LAMBDA_API_CRAWL_POST_COMMENT_PATH,
                         headers={},
                         body={},
                         request_schema=PostCommentAPIRequestSchema,
                         response_data_schema=PostCommentAPIResponseSchema)

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


class BasePageSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Int()
    app_id = fields.Int()
    username = fields.Str()
    avatar = fields.Str()


class BasePostSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Int()
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


class PostCommentAPIResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user = fields.Nested(BaseUserSchema)
    page = fields.Nested(BasePageSchema)

    post = fields.Nested(BasePostSchema, required=True)


class PostCommentAPIRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    post_app_id = fields.Str()
    social_type = fields.Str()
    account_info = fields.Dict()
    cursor = fields.Str()

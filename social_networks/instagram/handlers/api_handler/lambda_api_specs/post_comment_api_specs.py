from marshmallow import Schema, fields, EXCLUDE

from core.handlers.api_handler.api_specs.base_api_specs import BaseAPISpecs
from social_networks.instagram.utils.constant import Constant


class PostCommentAPISpecs(BaseAPISpecs):
    def __init__(self):
        super().__init__(method='post',
                         path=Constant.LAMBDA_API_CRAWL_POST_COMMENT_PATH,
                         headers={},
                         body={},
                         request_schema=PostCommentAPIRequestSchema,
                         response_schema=PostCommentAPIResponseSchema)

    def set_body(self, shortcode: str, cursor: str, account_info: dict, social_type=Constant.SOCIAL_TYPE_PROFILE):
        self.body = {'shortcode': shortcode,
                     'num_item': Constant.DEFAULT_PAGING_NUM_ITEM,
                     'social_type': social_type,
                     'account_info': account_info,
                     'cursor': cursor
                     }

    def set_headers(self, api_key):
        self.headers = {'X-API-KEY': api_key}


class PostCommentAPIResponseDataItemSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    comment = fields.Dict(required=True)
    user = fields.Dict()


class PostCommentAPIResponsePagingItemSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    has_next_page = fields.Bool(required=True)
    next_cursor = fields.Str(required=True, allow_none=True)


class PostCommentAPIResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    data = fields.List(fields.Nested(PostCommentAPIResponseDataItemSchema), required=True)
    paging = fields.Dict(required=True)


class PostCommentAPIRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    shortcode = fields.Str()
    num_item = fields.Int()
    account_info = fields.Dict(allow_none=True)
    cursor = fields.Str(allow_none=True)

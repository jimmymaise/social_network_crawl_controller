from marshmallow import Schema, fields, EXCLUDE

from core.handlers.api_handler.api_specs.base_api_specs import BaseAPISpecs
from social_networks.tiktok.utils.constant import Constant


class UserPostsAPISpecs(BaseAPISpecs):
    def __init__(self):
        super().__init__(method='post',
                         path=Constant.LAMBDA_API_CRAWL_USER_POSTS_PATH,
                         headers={},
                         body={},
                         request_schema=UserDetailAPIRequestSchema,
                         response_schema=UserDetailAPIResponseSchema)

    def set_body(self, sec_uid: str, cursor: int):
        self.body = {
            'sec_uid': sec_uid
        }

        if cursor is not None:
            self.body['cursor'] = cursor

    def set_headers(self, api_key):
        self.headers = {'X-API-KEY': api_key}


class UserDetailStatSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    follower_count = fields.Int(required=True)
    following_count = fields.Int()
    heart = fields.Int()
    heart_count = fields.Int()
    video_count = fields.Int()
    digg_count = fields.Int()


class BaseUserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Str(required=True)
    short_id = fields.Str()
    unique_id = fields.Str()
    username = fields.Str()
    nickname = fields.Str()
    sec_uid = fields.Str()
    avatar_larger = fields.Str()
    avatar_medium = fields.Str()
    avatar_thumb = fields.Str()
    signature = fields.Str()
    create_time = fields.Int()
    verified = fields.Bool()
    ftc = fields.Bool()
    relation = fields.Int()
    open_favorite = fields.Bool()
    bio_link = fields.Dict()
    comment_setting = fields.Int()
    duet_setting = fields.Int()
    stitch_setting = fields.Int()
    private_account = fields.Bool()
    secret = fields.Bool()
    room_id = fields.Str()
    stats = fields.Nested(UserDetailStatSchema)


class UserDetailAPIResponseDataItemSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user = fields.Nested(BaseUserSchema, required=True)
    post = fields.Dict()


class UserDetailAPIResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    data = fields.List(fields.Nested(UserDetailAPIResponseDataItemSchema, required=True))


class UserDetailAPIRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    username = fields.Str()
    cursor = fields.Int(allow_none=True)

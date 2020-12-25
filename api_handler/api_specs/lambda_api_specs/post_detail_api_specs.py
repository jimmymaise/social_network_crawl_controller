from marshmallow import Schema, fields, EXCLUDE


class APIPath:
    FB_POST_DETAIL = 'post_detail'


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

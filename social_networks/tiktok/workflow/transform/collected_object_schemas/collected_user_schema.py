from marshmallow import Schema, fields, EXCLUDE


class UserStatSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    follower_count = fields.Int(required=True)
    following_count = fields.Int()
    heart = fields.Int()
    heart_count = fields.Int()
    video_count = fields.Int()
    digg_count = fields.Int()


class UserObjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    stats = fields.Nested(UserStatSchema)
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

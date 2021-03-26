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

    _id = fields.Str(required=True)
    username = fields.Str()
    full_name = fields.Str()
    sec_uid = fields.Str()
    short_id = fields.Str()
    avatar = fields.Str()
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
    num_follower = fields.Int()
    num_following = fields.Int()
    num_likes = fields.Int()
    num_post = fields.Int()
    stats = fields.Nested(UserStatSchema)

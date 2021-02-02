from marshmallow import Schema, fields, EXCLUDE


class UserObjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Int(required=True)
    username = fields.Str(required=True)
    avatar = fields.Str()
    mini_avatar = fields.Str()
    full_name = fields.Str()
    bio = fields.Str()
    location = fields.List(fields.Dict())
    num_follower = fields.Int()
    num_following = fields.Int()
    num_post = fields.Int()
    is_verify = fields.Bool()
    is_business_account = fields.Bool()
    user_type = fields.Str()

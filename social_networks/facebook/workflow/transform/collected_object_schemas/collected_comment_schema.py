from marshmallow import Schema, fields, EXCLUDE


class CommentObjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Str()
    fbid = fields.Int()
    post_id = fields.Int()
    created_time = fields.Str()
    message = fields.Str()
    num_reaction = fields.Int()
    taken_at_timestamp = fields.Int()
    sticker = fields.Str()
    parent_comment_id = fields.Str()
    user_id = fields.Int()
    full_name = fields.Str()
    username = fields.Str()

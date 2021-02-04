from marshmallow import Schema, fields, EXCLUDE


class CommentObjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Str(required=True)
    user_id = fields.Int(required=True)
    post_id = fields.Int(required=True)
    message = fields.Str(required=True)
    taken_at_timestamp = fields.Int()

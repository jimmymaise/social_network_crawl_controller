from marshmallow import Schema, fields, EXCLUDE


class PostObjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Int()
    shortcode = fields.Str(required=True)
    user_id = fields.Int()
    post_type = fields.Str()
    content = fields.List(fields.Str())
    taken_at_timestamp = fields.Int()
    display_url = fields.Str()
    num_like = fields.Int(required=True)
    num_comment = fields.Int(required=True)
    num_crawled_comment = fields.Int()
    num_crawled_like = fields.Int()

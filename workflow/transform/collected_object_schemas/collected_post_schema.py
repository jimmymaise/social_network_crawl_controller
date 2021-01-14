from marshmallow import Schema, fields, EXCLUDE


class PostObjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Int()
    app_id = fields.Int()
    user_id = fields.Int()
    page_id = fields.Int()
    content = fields.Str()
    created_time = fields.Str()
    description = fields.Str()
    _from = fields.Dict()
    full_picture = fields.Str()
    hashtag = fields.List(fields.Str)
    is_hidden = fields.Bool()
    link = fields.Str()
    location = fields.Dict()
    num_comment = fields.Int()
    num_reaction = fields.Int()
    num_share = fields.Int()
    object_id = fields.Int()
    page_url = fields.Str()
    parent_id = fields.Str()
    permalink = fields.Str()
    post_type = fields.Str()
    properties = fields.List(fields.Dict)
    source = fields.Str()
    status_type = fields.Str()
    story = fields.Str()
    taken_at_timestamp = fields.Str()
    to = fields.Str()
    updated_time = fields.Str()
    via = fields.Str()

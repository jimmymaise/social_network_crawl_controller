from marshmallow import Schema, fields, EXCLUDE


class UsersObjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Int(required=True)
    app_id = fields.Int(required=True)
    avatar = fields.Str()
    cover = fields.Str()
    full_name = fields.Str().required
    location = fields.Dict()
    num_follower = fields.Int()
    page_url = fields.Str()
    username = fields.Str(required=True)
    work = fields.Dict()
    crawl_post_code = fields.Int()
    latest_posts = fields.List(dict)
    birthday = fields.Str()
    mini_avatar = fields.Str()
    num_photo = fields.Str()
    fake = fields.Str()
    is_public = fields.Str()
    branded_post = fields.Str()
    last_time_crawl_reaction = fields.Str()

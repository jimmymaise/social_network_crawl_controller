from marshmallow import Schema, fields, EXCLUDE


class UserObjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Int(required=True)
    username = fields.Str(required=True)
    avatar = fields.Str()
    mini_avatar = fields.Str()
    cover = fields.Str()
    full_name = fields.Str()
    location = fields.Dict()
    num_follower = fields.Int()
    page_url = fields.Str()
    work = fields.Dict()
    crawl_post_status = fields.Str()
    crawl_post_code = fields.Int()
    latest_posts = fields.List(fields.Dict)
    last_time_crawl_post = fields.Int()
    crawl_reaction_status = fields.Str()
    last_time_normalize = fields.Int()
    living_location = fields.Str()
    birthday = fields.Dict()
    about = fields.Str()
    num_photo = fields.Int()
    interest_category = fields.Dict()
    is_public = fields.Str()
    last_time_crawl_reaction = fields.Str()
    fake = fields.Str()
    branded_post = fields.Str()



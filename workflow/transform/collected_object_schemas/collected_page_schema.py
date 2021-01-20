from marshmallow import Schema, fields, EXCLUDE


class PageObjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Int()
    link = fields.Str()
    crawl_profile_status = fields.Str()
    about = fields.Str()
    app_id = fields.Int(required=True)
    category = fields.Str()
    category_list = fields.List(fields.Str())
    crawl_profile_code = fields.Int()
    fan_count = fields.Int()
    fb_link = fields.Str()
    location = fields.Dict()
    page_url = fields.Str()
    username = fields.Str(required=True)
    last_time_crawl_profile = fields.Int()
    crawl_priority_score = fields.Int()

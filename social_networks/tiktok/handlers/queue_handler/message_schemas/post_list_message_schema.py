from marshmallow import Schema, fields, EXCLUDE


class PostListMessageSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    service_name = fields.Str(required=True)
    hiip_user_id = fields.Int(required=True)
    country_code = fields.Str(required=True)
    social_type = fields.Str(required=True)
    social_id = fields.Str(required=False)
    social_user_name = fields.Str(required=True)
    sec_uid = fields.Str(required=True)

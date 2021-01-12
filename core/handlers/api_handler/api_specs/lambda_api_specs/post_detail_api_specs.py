from marshmallow import Schema, fields, EXCLUDE

from core.handlers.api_handler.api_specs.base_api_specs import BaseAPISpecs


class PostDetailAPISpecs(BaseAPISpecs):
    def __init__(self):
        super().__init__(method='post',
                         path='fb-post-details',
                         headers={},
                         body={},
                         request_schema=PostDetailAPIRequestSchema,
                         response_data_key='collected_data',
                         response_data_schema=PostDetailAPIResponseSchema)

    def set_body(self, post_link: str, account_info: dict):
        # todo Remove hardcode for testing purpose
        self.body = {'link': post_link,
                     'type': 'user',
                     'cookie': account_info.get('token') if account_info else None
                     or 'EAAAAZAw4FxQIBANYWnh5BTFIwTUb1IgkjLo1baRFEI1h57C51XqAgna1rNZB4TnnVb9Ya6OuMvcQBEmWEYHTBFq7QWK4VZBl3SI26fvuOBUETOlLcyzVFQnyqtaIdbN3RCaVZCpKkrRBscCGZCF1GCCZBVHukT49d42eJKmU2ZBpQZDZD'
                     }

    def set_headers(self, api_key):
        self.headers = {'X-API-KEY': api_key}


class BaseUserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    username = fields.Str()
    user_id = fields.Int()
    avatar = fields.Str()


class BasePostSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    content = fields.Str()
    full_picture = fields.Str()
    num_reaction = fields.Int()
    num_comment = fields.Int()
    num_share = fields.Int()
    view_count = fields.Int()
    feedback_id = fields.Str()


class BaseStatusSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    status_code = fields.Int()
    cookie_status = fields.Int()
    details = fields.Str()


class PostDetailAPIResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user = fields.Nested(BaseUserSchema)
    post = fields.Nested(BasePostSchema)


class PostDetailAPIRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    pass

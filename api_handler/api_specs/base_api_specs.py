from marshmallow import Schema, fields, EXCLUDE


class BaseAPISpecs:
    method: str
    path: str
    header: dict
    body: dict
    request_schema: object
    response_schema: object

    def __init__(self, method, path, header, body, request_schema, response_schema):
        self.method = method
        self.path = path
        self.body = body
        self.header = header
        self.request_schema = request_schema
        self.response_schema = response_schema

    def set_body(self, body):
        self.body = body

    def set_header(self, header):
        self.header = header


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
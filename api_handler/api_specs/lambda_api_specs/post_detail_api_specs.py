from marshmallow import Schema, fields, EXCLUDE

from api_handler.api_specs.base_api_specs import BaseAPISpecs, BaseUserSchema, BasePostSchema


class PostDetailAPISpecs(BaseAPISpecs):
    def __init__(self):
        super().__init__(method='POST',
                         path='post_detail',
                         header={},
                         body={},
                         request_schema=PostDetailAPIRequestSchema,
                         response_schema=PostDetailAPIResponseSchema)
        self.set_body({})
        self.set_header({})


class PostDetailAPIResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user = fields.Nested(BaseUserSchema)
    post = fields.Nested(BasePostSchema)


class PostDetailAPIRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    pass

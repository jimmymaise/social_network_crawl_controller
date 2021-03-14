from marshmallow import Schema, fields, EXCLUDE


class ToInt(fields.Int):
    """Field that serializes to a title case string and deserializes
    to a lower case string.
    """
    def _deserialize(self, value, attr, data, **kwargs):
        return int(value)


class InteractionSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    _id = fields.Str(required=True)
    average_view = ToInt(required=True)
    average_like = ToInt(required=True)
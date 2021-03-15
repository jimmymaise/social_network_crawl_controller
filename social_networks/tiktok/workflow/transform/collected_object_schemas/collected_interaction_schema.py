from marshmallow import Schema, fields, EXCLUDE


class ToInt(fields.Int):
    """Field that serializes to a title case string and deserializes
    to a lower case string.
    """
    def _deserialize(self, value, attr, data, **kwargs):
        return int(value)


def calculate_rate(average, num_follower):
    if num_follower is None or num_follower == 0:
        return 0

    return int(average / num_follower * 100)


class InteractionSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    _id = fields.Str(required=True)
    average_view = ToInt(required=True)
    average_view_rate = fields.Function(lambda obj: calculate_rate(obj['average_view'], obj['num_follower']))
    average_like = ToInt(required=True)
    average_like_rate = fields.Function(lambda obj: calculate_rate(obj['average_like'], obj['num_follower']))
    average_comment = ToInt(required=True)
    average_comment_rate = fields.Function(lambda obj: calculate_rate(obj['average_comment'], obj['num_follower']))
    average_share = ToInt(required=True)
    average_share_rate = fields.Function(lambda obj: calculate_rate(obj['average_share'], obj['num_follower']))
    average_engagement = fields.Function(
        lambda obj: int(obj['average_like'] + obj['average_comment'] + obj['average_share'])
    )
    average_engagement_rate = fields.Function(
        lambda obj: calculate_rate(int(obj['average_like'] + obj['average_comment'] + obj['average_share']),
                                   obj['num_follower'])
    )
    analyzed_post_to = fields.Int(required=True)
    analyzed_post_from = fields.Int(required=True)

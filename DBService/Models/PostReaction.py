# Import Models
from DBService.Models.BaseModel import BaseModel
from DBService.Models.ReactionTypeEnum import ReactionTypeEnum


class PostReactionModel(BaseModel):
    structure = [
        ['_id', '_id', int],  # Id of post
        ['post_id', 'post_id', int],  # post_id
        ['user_id', 'user_id', int],  # user_id of post
        ['type', 'type', str]  # type of reaction: like, haha, love, angry, wow, sad
    ]

    required_fields = ['_id', 'post_id', 'user_id']

    default_values = [
        ['type', ReactionTypeEnum.Unknown]
    ]

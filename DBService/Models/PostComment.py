# Import Models
from DBService.Models.BaseModel import BaseModel


class PostCommentModel(BaseModel):
    structure = [
        ['_id', '_id', int],
        ['post_id', 'post_id', int],  # post_id
        ['comment_id', 'comment_id', str],  # comment_id
        ['user_id', 'user_id', int]  # user_id of comment
    ]

    required_fields = ['_id', 'post_id', 'comment_id', 'user_id']

    default_values = []

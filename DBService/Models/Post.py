# Import Models
from DBService.Models.BaseModel import BaseModel
from DBService.Models.PostTypeEnum import PostTypeEnum


class PostModel(BaseModel):
    structure = [
        ['_id', '_id', int],  # Id of post
        ['app_id', 'app_id', str],  # Facebook API's id
        ['user_id', 'user_id', int],  # user_id of post
        ['post_type', 'post_type', str],  # store post_type_id
        ['full_picture', 'full_picture', str],  # full_picture
        ['medias', 'medias', [str]],  # media_id if post has more than one image
        ['content', 'content', [str]],
        ['num_reaction', 'num_reaction', int],
        ['num_comment', 'num_comment', int],
        ['num_share', 'num_share', int],
        ['link', 'link', str],
        ['page_url', 'page_url', str],
        ['created_time', 'created_time', str],
        ['taken_at_timestamp', 'taken_at_timestamp', int]  # Time taken of post
    ]

    required_fields = ['_id', 'user_id']

    default_values = [
        ['post_type', PostTypeEnum.Photo],
        ['full_picture', None],
        ['medias', None],
        ['content', ''],
        ['num_reaction', 0],
        ['num_comment', 0],
        ['num_share', 0]
    ]

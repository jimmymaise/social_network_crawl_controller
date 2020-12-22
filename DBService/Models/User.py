# Import Models
from DBService.Models.BaseModel import BaseModel
from DBService.Models.GenderEnum import GenderTypeEnum


class UserModel(BaseModel):
    structure = [
        ['_id', 'id', int],  # Facebook's id of user
        ['username', 'username', str],  # Name display on instagram
        ['full_name', 'full_name', str],  # Full name of user
        ['intro', 'intro', str],
        ['bio', 'bio', str],
        ['avatar', 'avatar', str],  # Store media_id
        ['gender', 'gender', str],  # Store gender name
        ['age', 'age', int],
        ['location', 'location', str],
        ['num_follower', 'num_follower', int],
        ['latest_posts', 'latest_posts', [int]]  # Score of crawling comment
    ]

    required_fields = ['_id', 'user_id']

    default_values = [
        ['intro', ''],
        ['bio', ''],
        ['avatar', None],
        ['gender', GenderTypeEnum.Unknown],
        ['age', -1],
        ['location', ''],
        ['num_follower', 0],
    ]

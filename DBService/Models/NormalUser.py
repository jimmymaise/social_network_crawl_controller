# Import libs
from SuperUtils.HashHelper import HashHelper

# Import Models
from DBService.Models.BaseModel import BaseModel
from DBService.Models.CrawlStatusEnum import CrawlStatusEnum


class NormalUserModel(BaseModel):
    structure = [
        ['_id', 'id', int],  # _id in mongo
        ['user_id', 'user_id', int],  # user_id
        ['username', 'username', str],  # name of user
    ]

    required_fields = ['id', 'username']

    default_values = []

    @classmethod
    def create_with(cls,
                    _user_id,
                    _username,
                    _crawl_profile_status=CrawlStatusEnum.Created):
        user_obj = cls._create_empty()
        user_obj = cls._set_default(user_obj)
        user_obj['_id'] = HashHelper.hash(str(_user_id))
        user_obj['user_id'] = _user_id
        user_obj['username'] = _username
        user_obj['crawl_profile_status'] = _crawl_profile_status
        return user_obj

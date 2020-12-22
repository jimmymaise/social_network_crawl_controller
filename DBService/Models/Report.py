# Import Models
from DBService.Models.BaseModel import BaseModel


class ReportModel(BaseModel):
    structure = [
        ['_id', '_id', int],  # Instagram's id of user
        ['app_id', 'app_id', int],  # App id of user
        ['user_id', 'user_id', int],  # User id of user
        ['status', 'status', str],  # Status of this document
        ['post', 'post', str],  # Full name of user
    ]

    default_values = []

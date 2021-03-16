from core.workflows.loading.load.base_load_handler import BaseLoadHandler
from social_networks.tiktok.handlers.db_handler.user_db_handler import UserDBHandler
from social_networks.tiktok.utils.constant import Constant


class UserLoadHandler(BaseLoadHandler):
    def __init__(self, db_handler: UserDBHandler):
        super().__init__(db_handler)
        self.load_collection_name = Constant.COLLECTION_NAME_USER

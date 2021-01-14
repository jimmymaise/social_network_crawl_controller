# Import libs
from core.handlers.db_handler.base_db_handler import BaseDBHandler


class MediaDBHandler(BaseDBHandler):
    def __init__(self, db_username, db_name, db_password, db_host, db_port):
        super().__init__(db_username, db_name, db_password, db_host, db_port)
        self.collection = self.database['media']

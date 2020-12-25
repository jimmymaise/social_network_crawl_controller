# Import libs
from db_handler.base_db_handler import BaseDBHandler


class MediaDBHandler(BaseDBHandler):
    def __init__(self):
        super(MediaDBHandler, self).__init__()
        self.collection = self.database['medias']

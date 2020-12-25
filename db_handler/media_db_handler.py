# Import libs
from db_handler import general_db_handler


class MediaDBHandler(general_db_handler):
    def __init__(self):
        super(MediaDBHandler, self).__init__()
        self.collection = self.database['medias']

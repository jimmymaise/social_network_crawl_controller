# Import libs
from DBService.DBHandler.GeneralDBHandler import GeneralDBHandler


class MediaDBHandler(GeneralDBHandler):
    def __init__(self):
        super(MediaDBHandler, self).__init__()
        self.collection = self.database['medias']

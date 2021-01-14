# Import libs
from core.handlers.db_handler.base_db_handler import BaseDBHandler


class ReportDBHandler(BaseDBHandler):
    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.collection = self.database['reports']

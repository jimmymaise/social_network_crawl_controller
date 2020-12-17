from pymongo import MongoClient


class MongodbHandler:
    def __init__(self, connection_uri, database_name=None, **kwargs):
        self.mongo_client = MongoClient(connection_uri)
        self.database_name = database_name

    def get_client(self):
        return self.mongo_client

    def get_db(self):
        if not self.database_name:
            raise ValueError('No Database has been set')
        return self.mongo_client[self.database_name]

    def set_db(self, database_name):
        self.database_name = database_name

    def get_items_by_query(self, query, collection_name):
        return []

from core.handlers.db_handler.base_db_handler import DBConnection
from core.handlers.db_handler.base_db_handler import GeneralDBHandler


class CollectionLookupHandler:

    def __init__(self, collection_name, db_connection: DBConnection):
        self.collection_name = collection_name
        self.db_connection = db_connection
        self.aggregate = []

    def add_lookup_field(self, lookup_field_name, collection_lookup,
                         field_name_local,
                         field_name_foreign,
                         field_name_return,
                         ):
        self.aggregate += [{'$lookup': {'from': collection_lookup,
                                        'localField': field_name_local,
                                        'foreignField': field_name_foreign,
                                        'as': lookup_field_name}},
                           {'$addFields': {
                               lookup_field_name: {'$arrayElemAt': [f'${lookup_field_name}.{field_name_return}', 0]}}}]
        return self

    def match(self, query_dict):
        self.aggregate += [
            {'$match': query_dict}]
        return self

    def query(self):
        db_handler = GeneralDBHandler(self.db_connection, self.collection_name)
        return list(db_handler.aggregate(self.aggregate))

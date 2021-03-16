import random
import string

from core.handlers.db_handler.base_db_handler import DBConnection
from core.handlers.db_handler.base_db_handler import GeneralDBHandler


class CollectionLookupHandler:

    def __init__(self, collection_name, db_connection: DBConnection):
        self.collection_name = collection_name
        self.db_connection = db_connection
        self.aggregate = []
        self.temp_fields = []

    def add_lookup_field(self, lookup_field_name, collection_lookup,
                         field_name_local,
                         field_name_foreign,
                         return_field_name,
                         ):
        temp_field = ''.join(random.choices(string.ascii_lowercase, k=9))

        self.aggregate += [{'$lookup': {'from': collection_lookup,
                                        'localField': field_name_local,
                                        'foreignField': field_name_foreign,
                                        'as': temp_field}},
                           {'$addFields': {
                               lookup_field_name: {'$arrayElemAt': [f'${temp_field}.{return_field_name}', 0]}}}]
        self.temp_fields.append(temp_field)

        return self

    def add_lookup_multiple_fields(self, lookup_field_names, collection_lookup,
                                   field_name_local,
                                   field_name_foreign,
                                   return_field_names,
                                   ):
        if len(lookup_field_names) != len(return_field_names):
            raise ValueError('size of lookup_field_names and return_field_names must equal')

        temp_field = ''.join(random.choices(string.ascii_lowercase, k=9))
        self.aggregate.append({'$lookup': {'from': collection_lookup,
                                           'localField': field_name_local,
                                           'foreignField': field_name_foreign,
                                           'as': temp_field}})

        add_fields = {}
        for index, lookup_field_name in enumerate(lookup_field_names):
            add_fields[lookup_field_name] = {'$arrayElemAt': [f'${temp_field}.{return_field_names[index]}', 0]}

        self.aggregate.append({'$addFields': add_fields})
        self.temp_fields.append(temp_field)

        return self

    def match(self, query_dict):
        self.aggregate += [
            {'$match': query_dict}]
        return self

    def query(self):
        db_handler = GeneralDBHandler(self.db_connection, self.collection_name)
        query_result = list(db_handler.aggregate(self.aggregate))
        for item in query_result:
            for temp_field in self.temp_fields:
                item.pop(temp_field, None)
        return query_result

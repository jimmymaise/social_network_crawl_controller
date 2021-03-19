# Import libs
import urllib.parse

from pymongo import MongoClient
from pymongo import UpdateOne, DeleteOne

from core.utils.constant import Constant


# Import config


class DBConnection(object):

    def __init__(self, db_host, db_port, db_name, db_username, db_password):
        if db_username and db_password:
            db_username = urllib.parse.quote_plus(db_username)
            db_password = urllib.parse.quote_plus(db_password)
            host_address = f'mongodb://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
        else:
            host_address = f'mongodb://{db_host}:{db_port}/{db_name}'
        self.client = MongoClient(host_address, connect=False)
        self.db = self.client[db_name]


class BaseDBHandler(object):
    def __init__(self, connection: DBConnection):
        self.client = connection.client
        self.database = connection.db
        self.collection = None

    def aggregate(self, aggregate: list):
        return self.collection.aggregate(aggregate)

    def get_one_by_filter(self,
                          filter_,
                          sort_,
                          limit=None,
                          selected_fields=None,
                          must_have_fields=None,
                          not_have_fields=None):

        return self._get_one_or_many_by_filter(filter_=filter_, sort_=sort_, limit=limit,
                                               selected_fields=selected_fields,
                                               must_have_fields=must_have_fields,
                                               not_have_fields=not_have_fields,
                                               find_type=Constant.MONGODB_FIND_TYPE_FIND_ONE,
                                               )

    def get_many_by_filter(self,
                           filter_,
                           sort_=None,
                           limit=None,
                           selected_fields=None,
                           must_have_fields=None,
                           not_have_fields=None):

        return self._get_one_or_many_by_filter(filter_=filter_, sort_=sort_, limit=limit,
                                               selected_fields=selected_fields,
                                               must_have_fields=must_have_fields,
                                               not_have_fields=not_have_fields,
                                               find_type=Constant.MONGODB_FIND_TYPE_FIND_MANY,
                                               )

    def _get_one_or_many_by_filter(self,
                                   find_type,
                                   **get_by_filter_kwargs
                                   ):
        filter_ = get_by_filter_kwargs['filter_']
        must_have_fields = get_by_filter_kwargs.get('must_have_fields')
        not_have_fields = get_by_filter_kwargs.get('not_have_fields')
        selected_fields = get_by_filter_kwargs.get('selected_fields')
        sort_ = get_by_filter_kwargs.get('sort_')
        limit = get_by_filter_kwargs.get('limit')

        for must_have_field in (must_have_fields or []):
            filter_[must_have_field] = {'$exists': True}

        for not_have_field in (not_have_fields or []):
            filter_[not_have_field] = {'$exists': False}

        selected_fields_dict = self._create_fields_dict(selected_fields) if selected_fields else None
        collection_find = getattr(self.collection, find_type)(filter_, selected_fields_dict)

        if find_type == Constant.MONGODB_FIND_TYPE_FIND_ONE:
            return collection_find

        if sort_:
            collection_find = collection_find.sort(sort_)
        return collection_find.limit(limit or 0)

    def insert_one(self,
                   one_info):
        result = self.collection.insert_one(one_info)
        return result

    def insert_many(self,
                    many_info):
        result = self.collection.insert_many(many_info)
        return result

    def delete_one(self,
                   one_info):
        result = self.collection.delete_one(one_info)
        return result

    def delete_many(self,
                    many_info):
        result = self.collection.delete_many(many_info)
        return result

    def update_one(self,
                   _updated_record,
                   upsert=False):
        result = self.update_many_pair(updated_records=[_updated_record],
                                       upsert=upsert)
        return result

    def update_many(self,
                    many_info):
        result = self.collection.update_many(many_info)
        return result

    def update_many_pair(self,
                         updated_records,
                         upsert=False,
                         collation=None,
                         array_filters=None,
                         operator='$set'):
        # ===== Execute =====
        requests = [UpdateOne(filter_,
                              {operator: updated_record},
                              upsert=upsert,
                              collation=collation,
                              array_filters=array_filters)
                    for filter_, updated_record in updated_records]

        result = self.bulk_write(requests)
        return result

    def find_or_create_many_pair(self,
                                 updated_records,
                                 upsert=False):
        # ===== Execute =====
        requests = [UpdateOne(filter_,
                              {'$setOnInsert': updated_record},
                              upsert=upsert)
                    for filter_, updated_record in updated_records]

        result = self.bulk_write(requests)
        return result

    def update(self,
               filter_,
               _new_info,
               _multi=False):
        result = self.collection.update(spec=filter_,
                                        document=_new_info,
                                        multi=_multi)
        return result

    def bulk_write(self,
                   requests):
        if requests:
            result = self.collection.bulk_write(requests)
        else:
            result = None
        return result

    def get_many_pairs_by_id(self,
                             _ids,
                             filter_=None,
                             selected_fields=None,
                             must_have_fields=None,
                             not_have_fields=None):
        filter_record = {'_id': {'$in': _ids}}

        if isinstance(filter_, dict):
            for key, value in filter_.items():
                filter_record[key] = value
        result = self.get_many_by_filter(filter_=filter_record,
                                         selected_fields=selected_fields,
                                         must_have_fields=must_have_fields,
                                         not_have_fields=not_have_fields)
        return result

    def get_one_by_id(self,
                      _id,
                      selected_fields=None):
        result = self.get_one_by_filter(filter_={'_id': _id},
                                        selected_fields=selected_fields)
        return result

    def get_one_by_app_id(self,
                          app_id,
                          selected_fields=None):
        result = self.get_one_by_filter(filter_={'app_id': app_id},
                                        selected_fields=selected_fields)
        return result

    def delete_many_pair(self,
                         _delete_records):
        # ===== Exec =====
        requests = [DeleteOne(_delete_record)
                    for _delete_record in _delete_records]
        service_result = self.bulk_write(requests)
        return service_result

    @staticmethod
    def _create_fields_dict(selected_fields):
        selected_fields_dict = {}
        for selected_field in selected_fields:
            selected_fields_dict[selected_field] = 1
        return selected_fields_dict

    def count_by_filter(self,
                        filter_):
        result = self.get_many_by_filter(filter_).count(True)
        return result

    # Refactor from here
    def bulk_write_many_update_objects(self, update_objects):
        if not update_objects:
            return

        requests = [UpdateOne(filter=update_object['filter'],
                              update={update_object.get('operator', '$set'): update_object['update']},
                              upsert=update_object.get('upsert', True),
                              collation=update_object.get('collation'),
                              array_filters=update_object.get('array_filters'))
                    for update_object in update_objects]

        result = self.bulk_write(requests)
        return result

    def close_connection(self):
        """Close connection after done"""
        self.client.close()


class GeneralDBHandler(BaseDBHandler):
    def __init__(self, connection, collection_name):
        super().__init__(connection)
        self.collection = self.database[collection_name]

# Import libs
import urllib.parse

from pymongo import MongoClient
from pymongo import UpdateOne, DeleteOne


# Import config


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBConnection(object):
    __metaclass__ = Singleton

    def __init__(self, db_host, db_port, db_name, db_username, db_password):
        if db_username and db_password:
            db_username = urllib.parse.quote_plus(db_username)
            db_password = urllib.parse.quote_plus(db_password)
            host_address = f'mongodb://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
        else:
            host_address = f'mongodb://{db_host}:{db_port}/{db_name}'
        self.client = MongoClient(host_address, connect=False)


class BaseDBHandler(object):
    # ********** Constructor **********
    def __init__(self, db_username, db_name, db_password, db_host, db_port):
        _connection = DBConnection(db_host, db_port, db_name, db_username, db_password)
        self.client = _connection.client
        self.database = self.client['facebook']
        self.collection = None

    def get_one_by_filter(self,
                          filter_,
                          selected_fields=None):
        if selected_fields is None:
            result = self.collection.find_one(filter_)
        else:
            selected_fieldsdict = self._create_fields_dict(selected_fields)
            result = self.collection.find_one(filter_, selected_fieldsdict)
        return result

    def get_many_by_filter(self,
                           filter_,
                           selected_fields=None,
                           must_have_fields=None,
                           not_have_fields=None):
        if must_have_fields:
            for _must_have_field in must_have_fields:
                filter_[_must_have_field] = {'$exists': True}
        if not_have_fields:
            for _not_have_field in not_have_fields:
                filter_[_not_have_field] = {'$exists': False}
        if selected_fields is None:
            result = self.collection.find(filter_)
        else:
            selected_fieldsdict = self._create_fields_dict(selected_fields)
            result = self.collection.find(filter_, selected_fieldsdict)
        return result

    def get_many_by_filter_and_sort(self,
                                    filter_,
                                    sort_,
                                    limit_=None,
                                    selected_fields=None,
                                    must_have_fields=None,
                                    not_have_fields=None):
        if must_have_fields:
            for _must_have_field in must_have_fields:
                filter_[_must_have_field] = {'$exists': True}
        if not_have_fields:
            for _not_have_field in not_have_fields:
                filter_[_not_have_field] = {'$exists': False}
        if selected_fields is None:
            result = self.collection.find(filter_)
        else:
            selected_fields_dict = self._create_fields_dict(selected_fields)
            result = self.collection.find(filter_, selected_fields_dict).sort(sort_)
        return result

    def insert_one(self,
                   _one_info):
        result = self.collection.insert_one(_one_info)
        return result

    def insert_many(self,
                    _many_info):
        result = self.collection.insert_many(_many_info)
        return result

    def delete_one(self,
                   _one_info):
        result = self.collection.delete_one(_one_info)
        return result

    def delete_many(self,
                    _many_info):
        result = self.collection.delete_many(_many_info)
        return result

    def update_one(self,
                   _updated_record,
                   _upsert=False):
        result = self.update_many_pair(_updated_records=[_updated_record],
                                       _upsert=_upsert)
        return result

    def update_many(self,
                    _many_info):
        result = self.collection.update_many(_many_info)
        return result

    def update_many_pair(self,
                         _updated_records,
                         _upsert=False,
                         _write_concern=None,
                         _collation=None,
                         _array_filters=None,
                         _operator='$set'):
        # ===== Execute =====
        _requests = [UpdateOne(filter_,
                               {_operator: _updated_record},
                               upsert=_upsert,
                               collation=_collation,
                               array_filters=_array_filters)
                     for filter_, _updated_record in _updated_records]

        result = self.bulk_write(_requests)
        return result

    def find_or_create_many_pair(self,
                                 _updated_records,
                                 _upsert=False):
        # ===== Execute =====
        _requests = [UpdateOne(filter_,
                               {'$setOnInsert': _updated_record},
                               upsert=_upsert)
                     for filter_, _updated_record in _updated_records]

        result = self.bulk_write(_requests)
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
                   _requests):
        if _requests:
            result = self.collection.bulk_write(_requests)
        else:
            result = None
        return result

    def aggregate(self,
                  _requests):
        result = self.collection.aggregate(_requests)
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
        result = self.get_one_by_filter(_filter={'_id': _id},
                                        selected_fields=selected_fields)
        return result

    def get_one_by_app_id(self,
                          app_id,
                          selected_fields=None):
        result = self.get_one_by_filter(_filter={'app_id': app_id},
                                        selected_fields=selected_fields)
        return result

    def delete_many_pair(self,
                         _delete_records):
        # ===== Exec =====
        _requests = [DeleteOne(_delete_record)
                     for _delete_record in _delete_records]
        service_result = self.bulk_write(_requests)
        return service_result

    @staticmethod
    def _create_fields_dict(selected_fields):
        selected_fieldsdict = {}
        for _selected_field in selected_fields:
            selected_fieldsdict[_selected_field] = 1
        return selected_fieldsdict

    def count_by_filter(self,
                        filter_):
        result = self.get_many_by_filter(filter_).count(True)
        return result

    # Refactor from here
    def bulk_write_many_update_objects(self, update_objects):
        if not update_objects:
            return
        _requests = [UpdateOne(filter=update_object['filter'],
                               update={update_object.get('operator', '$set'): update_object['update']},
                               upsert=update_object.get('upsert', True),
                               collation=update_object.get('collation'),
                               array_filters=update_object.get('array_filters'))
                     for update_object in update_objects]

        result = self.bulk_write(_requests)
        return result

    def close_connection(self):
        """Close connection after done"""
        self.client.close()

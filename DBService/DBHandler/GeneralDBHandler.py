# Import libs
from pymongo import MongoClient
from pymongo import UpdateOne, DeleteOne
import urllib.parse

# Import config
from DBService.Config.DBConfig import DBCONFIG


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBConnection(object):
    __metaclass__ = Singleton

    def __init__(self):
        if DBCONFIG['USERNAME'] and DBCONFIG['PASS']:
            username = urllib.parse.quote_plus(DBCONFIG['USERNAME'])
            password = urllib.parse.quote_plus(DBCONFIG['PASS'])
            _host_address = 'mongodb://%s:%s@%s:%s/%s' % (username,
                                                          password,
                                                          DBCONFIG['HOST'],
                                                          DBCONFIG['PORT'],
                                                          DBCONFIG['DATABASE'])
        else:
            _host_address = 'mongodb://%s:%s/%s' % (DBCONFIG['HOST'],
                                                    DBCONFIG['PORT'],
                                                    DBCONFIG['DATABASE'])
        self.client = MongoClient(_host_address, connect=False)


class GeneralDBHandler(object):
    # ********** Constructor **********
    def __init__(self):
        _connection = DBConnection()
        self.client = _connection.client
        self.database = self.client['facebook']
        self.collection = None

    def get_one_by_filter(self,
                          _filter,
                          _selected_fields=None):
        if _selected_fields is None:
            result = self.collection.find_one(_filter)
        else:
            _selected_fields_dict = self._create_fields_dict(_selected_fields)
            result = self.collection.find_one(_filter, _selected_fields_dict)
        return result

    def get_many_by_filter(self,
                           _filter,
                           _selected_fields=None,
                           _must_have_fields=None,
                           _not_have_fields=None):
        if _must_have_fields:
            for _must_have_field in _must_have_fields:
                _filter[_must_have_field] = {'$exists': True}
        if _not_have_fields:
            for _not_have_field in _not_have_fields:
                _filter[_not_have_field] = {'$exists': False}
        if _selected_fields is None:
            result = self.collection.find(_filter)
        else:
            _selected_fields_dict = self._create_fields_dict(_selected_fields)
            result = self.collection.find(_filter, _selected_fields_dict)
        return result

    def get_many_by_filter_and_sort(self,
                                    _filter,
                                    _sort,
                                    _selected_fields=None,
                                    _must_have_fields=None,
                                    _not_have_fields=None):
        if _must_have_fields:
            for _must_have_field in _must_have_fields:
                _filter[_must_have_field] = {'$exists': True}
        if _not_have_fields:
            for _not_have_field in _not_have_fields:
                _filter[_not_have_field] = {'$exists': False}
        if _selected_fields is None:
            result = self.collection.find(_filter)
        else:
            _selected_fields_dict = self._create_fields_dict(_selected_fields)
            result = self.collection.find(_filter, _selected_fields_dict).sort(_sort)
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
        _requests = [UpdateOne(_filter,
                               {_operator: _updated_record},
                               upsert=_upsert,
                               collation=_collation,
                               array_filters=_array_filters)
                     for _filter, _updated_record in _updated_records]

        result = self.bulk_write(_requests)
        return result

    def find_or_create_many_pair(self,
                                 _updated_records,
                                 _upsert=False):
        # ===== Execute =====
        _requests = [UpdateOne(_filter,
                               {'$setOnInsert': _updated_record},
                               upsert=_upsert)
                     for _filter, _updated_record in _updated_records]

        result = self.bulk_write(_requests)
        return result

    def update(self,
               _filter,
               _new_info,
               _multi=False):
        result = self.collection.update(spec=_filter,
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
                             _filter=None,
                             _selected_fields=None,
                             _must_have_fields=None,
                             _not_have_fields=None):
        _filter_record = {'_id': {'$in': _ids}}

        if isinstance(_filter, dict):
            for _key, _value in _filter.items():
                _filter_record[_key] = _value
        result = self.get_many_by_filter(_filter=_filter_record,
                                         _selected_fields=_selected_fields,
                                         _must_have_fields=_must_have_fields,
                                         _not_have_fields=_not_have_fields)
        return result

    def get_one_by_id(self,
                      _id,
                      _selected_fields=None):
        result = self.get_one_by_filter(_filter={'_id': _id},
                                        _selected_fields=_selected_fields)
        return result

    def get_one_by_app_id(self,
                          app_id,
                          _selected_fields=None):
        result = self.get_one_by_filter(_filter={'app_id': app_id},
                                        _selected_fields=_selected_fields)
        return result

    def delete_many_pair(self,
                         _delete_records):
        # ===== Exec =====
        _requests = [DeleteOne(_delete_record)
                     for _delete_record in _delete_records]
        service_result = self.bulk_write(_requests)
        return service_result

    @staticmethod
    def _create_fields_dict(_selected_fields):
        selected_fields_dict = {}
        for _selected_field in _selected_fields:
            selected_fields_dict[_selected_field] = 1
        return selected_fields_dict

    def count_by_filter(self,
                        _filter):
        result = self.get_many_by_filter(_filter).count(True)
        return result

    def close_connection(self):
        "Close connection after done"
        self.client.close()
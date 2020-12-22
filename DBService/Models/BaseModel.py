class BaseModel(object):
    structure       = []
    required_fields = []
    default_values  = {}

    @classmethod
    def _default_type(cls,
                      _type):
        if _type == int:
            return -1
        if _type == float:
            return 0.0
        if _type == str:
            return ''
        if _type == list:
            return []

    @classmethod
    def _create_empty(cls):
        user_obj = {}
        for _field in cls.structure:
            _db_field, _, _type = _field
            user_obj[_db_field] = cls._default_type(_type)
        return user_obj

    @classmethod
    def _set_default(cls,
                     _user_obj):
        user_obj = _user_obj
        for _field in cls.default_values:
            _key, _default_value = _field
            user_obj[_key] = _default_value() if callable(_default_value) else _default_value       # _default_value can be a function or value
        return user_obj

    @classmethod
    def create(cls):
        user_obj  = cls._create_empty()
        user_obj  = cls._set_default(user_obj)
        return user_obj

    @classmethod
    def _cast_type(cls,
                   _value,
                   _new_type):
        if isinstance(_value, _new_type):
            return _value
        if _new_type == int:
            return int(_value)
        if _new_type == float:
            return float(_value)
        if _new_type == str:
            return str(_value)
        if isinstance(_new_type, list):
            _new_list = []
            for _one_value in _value:
                _new_list.append(cls._cast_type(_one_value,
                                                _new_type[0]))
            return _new_list

    @classmethod
    def _transfer_data(cls,
                       _user_obj,
                       _data_obj):
        user_obj = _user_obj
        for _field in cls.structure:
            _db_field, _data_field, _type = _field
            if _data_field in _data_obj:
                user_obj[_db_field] = cls._cast_type(_data_obj[_data_field], _type)
        return user_obj

    @classmethod
    def parse_full(cls,
                   _data_obj):
        user_obj  = cls._create_empty()
        user_obj  = cls._set_default(user_obj)
        user_obj  = cls._transfer_data(user_obj, _data_obj)
        return user_obj

    @classmethod
    def parse_mini(cls,
                   _data_obj):
        user_obj = {}
        user_obj = cls._transfer_data(user_obj, _data_obj)
        return user_obj

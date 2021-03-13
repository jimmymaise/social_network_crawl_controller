# Import libs
import base64
import hashlib
import json
from pathlib import Path


class Common:
    @staticmethod
    def warning_when_retry(self, retry_object, sleep, last_result):
        self.logger.warning(
            'Retrying %s: last_result=%s, retrying in %s seconds...',
            retry_object.fn, last_result, sleep)

    @classmethod
    def md5_hash(cls, str_input):
        if isinstance(str_input, str):
            str_input = str_input.encode()

        hash_object = base64.b64encode(hashlib.md5(str_input).digest())
        result = hash_object.decode()
        return result

    @staticmethod
    def get_project_root() -> Path:
        return Path(__file__).parents[2]

    @staticmethod
    def validate_schema(data, schema):
        error = {}
        try:
            schema().load(data)
        except Exception as e:
            error = e
        return data, error

    @staticmethod
    def parse_base_64_json_string_to_dict(input_str):
        return json.loads(base64.b64decode(input_str))

    @staticmethod
    def transform_dict_with_mapping(dict_, mapping, default_value=None):
        transformed_dict = {k: dict_.get(v, default_value) for k, v in mapping.items()}
        return transformed_dict


class Dict2Obj:
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __repr__(self):
        """"""
        return "<Dict2Obj: %s>" % self.__dict__

    def __getitem__(self, key):
        return self.__dict__[key]

# Import libs
import base64
import hashlib


class Common:
    @staticmethod
    def warning_when_retry(self, retry_object, sleep, last_result):
        self.logger.warning(
            'Retrying %s: last_result=%s, retrying in %s seconds...',
            retry_object.fn, last_result, sleep)

    @classmethod
    def hash_url(cls,
                 _str):
        _str = _str.encode()
        hash_object = base64.b64encode(hashlib.md5(_str).digest())
        result = hash_object.decode()
        return result

# Import libs
import time

# Import Models
from DBService.Models.BaseModel import BaseModel
from DBService.Models.CountryCodeEnum import CountryCodeEnum

# Import Utils
from SuperUtils.HashHelper import HashHelper


class KOLModel(BaseModel):
    structure = [
        ['_id', 'id', int],  # _id in mongo
        ['app_id', 'app_id', int],  # app_id of Facebook API
        ['user_id', 'user_id', int],  # user_id
        ['username', 'username', str],  # name of user
        ['country_code', 'country_code', str]  # country of user
    ]

    required_fields = ['_id', 'username']

    default_values = [
        ['country_code', None]
    ]

    @classmethod
    def _get_country_code(cls,
                          _code):
        if not isinstance(_code, unicode) or _code is None:
            return CountryCodeEnum.UN
        if _code.upper() == 'VI':
            return CountryCodeEnum.VI
        if _code.upper() == 'TH':
            return CountryCodeEnum.TH
        if _code.upper() == 'ID':
            return CountryCodeEnum.ID
        return CountryCodeEnum.UN

    @classmethod
    def create_with(cls,
                    _hiip_user_id=None,
                    _app_id=None,
                    _country_code=None,
                    _username=None,
                    _priority=0):
        kol_obj = cls._create_empty()
        kol_obj = cls._set_default(kol_obj)
        kol_obj['priority'] = _priority

        # --- Save hiip user id ---
        if _hiip_user_id:
            kol_obj['hiip_user_id'] = _hiip_user_id

        # --- Save app id ---
        if _app_id:
            kol_obj['app_id'] = _app_id

        # --- Save username ---
        if _username:
            kol_obj['username'] = _username

        # --- Save country code ---
        if _country_code:
            kol_obj['country_code'] = [cls._get_country_code(_country_code)]
        else:
            raise ValueError('Country code is None!')

        # --- Create _id ----
        _current_timestamp = int(time.time())
        if _hiip_user_id:
            kol_obj['_id'] = HashHelper.hash(str(_hiip_user_id) + str(_current_timestamp))
        elif _app_id:
            kol_obj['_id'] = HashHelper.hash(str(_app_id))
        elif _username:
            kol_obj['_id'] = HashHelper.hash(_username)
        else:
            raise ValueError('App id and username are None!')

        return kol_obj

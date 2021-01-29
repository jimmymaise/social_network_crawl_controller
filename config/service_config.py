import base64
import json
import os
from pathlib import Path

from config.service_config_local import RUN_LOCAL_SERVICE
from core.utils.constant import Constant


class ServiceConfigs:

    @staticmethod
    def get_service_config() -> dict:
        if os.environ.get('SERVICE_CONFIG'):
            return json.loads(base64.b64decode(os.environ.get('SERVICE_CONFIG')))
        service_config_file_path = f'{str(Path(__file__).resolve().parents[0])}' \
                                   f'/{Constant.SERVICE_CONFIG_FOLDER_NAME}/{RUN_LOCAL_SERVICE}.json'
        with open(service_config_file_path, 'r') as service_config_file:
            service_config_str = service_config_file.read()
            return json.loads(service_config_str)

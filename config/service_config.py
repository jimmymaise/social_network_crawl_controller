import base64
import json
import os

from config.system_config import SystemConfig
from core.utils.common import Common
from core.utils.constant import Constant


class ServiceConfigs:

    @staticmethod
    def get_service_config() -> dict:
        if os.environ.get('SERVICE_CONFIG'):
            return json.loads(base64.b64decode(os.environ.get('SERVICE_CONFIG')))

        elif os.environ.get('ENV', '').lower() == 'local':
            service_config_file_path = f'{Common.get_project_root()}/social_networks/' \
                                       f'{SystemConfig.get_system_config().SOCIAL_NETWORK.lower()}' \
                                       f'/{Constant.SERVICE_CONFIG_FOLDER_NAME}/' \
                                       f'{SystemConfig.get_system_config().DEFAULT_SERVICE_LOCAL}.json'
            with open(service_config_file_path, 'r') as service_config_file:
                service_config_str = service_config_file.read()
                return json.loads(service_config_str)
        raise Exception('Should have SERVICE_CONFIG if not running local')

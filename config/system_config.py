import os

from core.handlers.file_handler.file_handler import FileHandler
from core.utils.common import Common

lambda_config = {}


class SystemConfig:

    @staticmethod
    def get_system_config(social_network=None):
        global lambda_config

        if os.getenv('LAMBDA') and not lambda_config:
            config_path = f'{Common.get_project_root()}/config/lambda_social_network_configs/' \
                          f'{social_network.lower()}.env'
            lambda_config = FileHandler.load_env_file_to_dict(config_path)
            BaseSystemConfig.load_lambda_config()
        return BaseSystemConfig


class BaseSystemConfig:
    DEFAULT_SERVICE_LOCAL = os.getenv('DEFAULT_SERVICE_LOCAL', 'user_collection')
    SOCIAL_NETWORK = os.getenv('SOCIAL_NETWORK', 'TIKTOK')

    AM_BASE_URL = os.getenv('AM_BASE_URL', 'http://34.219.102.184:9099')

    MONGO_DB_HOST = os.getenv('MONGO_DB_HOST', 'localhost')
    MONGO_DB_PORT = os.getenv('MONGO_DB_PORT', 27017)
    MONGO_DB_DATABASE_NAME = os.getenv('MONGO_DB_DATABASE_NAME', 'tiktok')
    MONGO_DB_USERNAME = os.getenv('MONGO_DB_USERNAME')
    MONGO_DB_PASSWORD = os.getenv('MONGO_DB_PASSWORD')

    LAMBDA_BASE_URL = os.getenv('LAMBDA_BASE_URL',
                                'https://5j0ilnnh1l.execute-api.us-west-2.amazonaws.com/tt')
    LAMBDA_X_API_KEY = os.getenv('LAMBDA_X_API_KEY', 'Rcp9a7US932wBZtp5Dd7P8rN5rY02UQF3qIw8iBO')

    SLACK_NOTIFICATION_URL = os.getenv('SLACK_NOTIFICATION_URL',
                                       'https://hooks.slack.com/services/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'
                                       )
    SERVICE_SLEEP_INTERVAL = os.getenv('PROCESS_SLEEP_INTERVAL', 5)
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'hiip-asia-media')
    S3_IMAGE_PATH = os.getenv('S3_IMAGE_PATH', f'images/{SOCIAL_NETWORK.lower()}')
    QUEUE_NAME_USER_DATA_SYNC = os.getenv('QUEUE_NAME_USER_DATA_SYNC', 'user_data_sync')
    QUEUE_NAME_POST_LIST_COLLECTION = os.getenv('QUEUE_NAME_POST_LIST_COLLECTION', 'post_list_collection')

    @classmethod
    def load_lambda_config(cls):
        global lambda_config
        [setattr(cls, attr, lambda_config.get(attr, getattr(cls, attr))) for attr in dir(cls) if
         not callable(getattr(cls, attr)) and not attr.startswith("__")]

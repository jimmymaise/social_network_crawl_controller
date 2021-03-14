import os

from core.handlers.file_handler.file_handler import FileHandler
from core.utils.common import Common

lambda_config = {}


def get_config_by_key(key, default_value=None):
    if lambda_config:
        return lambda_config.get(key, default_value)
    return os.getenv('S3_BUCKET_NAME', default_value)


class SystemConfig:

    @staticmethod
    def get_system_config(social_network=None):
        global lambda_config

        if os.getenv('EN') and not lambda_config:
            config_path = f'{Common.get_project_root()}/config/social_network_configs/{social_network.lower()}.env'
            lambda_config = FileHandler.load_json_file_to_dict(config_path)
        return BaseSystemConfig


class BaseSystemConfig:
    DEFAULT_SERVICE_LOCAL = get_config_by_key('DEFAULT_SERVICE_LOCAL', 'user_collection')
    SOCIAL_NETWORK = get_config_by_key('SOCIAL_NETWORK', 'TIKTOK')

    AM_BASE_URL = get_config_by_key('AM_BASE_URL', 'http://34.219.102.184:9099')

    MONGO_DB_HOST = get_config_by_key('MONGODB_HOST', 'localhost')
    MONGO_DB_PORT = get_config_by_key('MONGODB_PORT', 27017)
    MONGO_DB_DATABASE_NAME = get_config_by_key('MONGODB_DB', 'tiktok')
    MONGO_DB_USERNAME = get_config_by_key('MONGODB_USER')
    MONGO_DB_PASSWORD = get_config_by_key('MONGODB_PASS')

    LAMBDA_BASE_URL = get_config_by_key('LAMBDA_BASE_URL',
                                        'https://5j0ilnnh1l.execute-api.us-west-2.amazonaws.com/tt')
    LAMBDA_X_API_KEY = get_config_by_key('LAMBDA_X_API_KEY', 'Rcp9a7US932wBZtp5Dd7P8rN5rY02UQF3qIw8iBO')

    SLACK_NOTIFICATION_URL = get_config_by_key('SLACK_NOTIFICATION_URL',
                                               'https://hooks.slack.com/services/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')
    SERVICE_SLEEP_INTERVAL = get_config_by_key('PROCESS_SLEEP_INTERVAL', 5)
    S3_BUCKET_NAME = get_config_by_key('S3_BUCKET_NAME', 'hiip-asia-media')
    S3_IMAGE_PATH = get_config_by_key('S3_IMAGE_PATH', f'images/{SOCIAL_NETWORK.lower()}')
    QUEUE_NAME_USER_DATA_SYNC = 'sync-new-user-data'
    QUEUE_NAME_POST_LIST_COLLECTION = 'sync-new-post-data'

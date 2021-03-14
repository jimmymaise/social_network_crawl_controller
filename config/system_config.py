import os


class SystemConfig:
    DEFAULT_SERVICE_LOCAL = os.environ.get('DEFAULT_SERVICE_LOCAL', 'user_collection')
    SOCIAL_NETWORK = os.environ.get('SOCIAL_NETWORK', 'TIKTOK')

    AM_BASE_URL = os.getenv('AM_BASE_URL', 'http://34.219.102.184:9099')

    MONGO_DB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
    MONGO_DB_PORT = os.environ.get('MONGODB_PORT', 27017)
    MONGO_DB_DATABASE_NAME = os.environ.get('MONGODB_DB', 'tiktok')
    MONGO_DB_USERNAME = os.environ.get('MONGODB_USER')
    MONGO_DB_PASSWORD = os.environ.get('MONGODB_PASS')

    LAMBDA_BASE_URL = os.environ.get('LAMBDA_BASE_URL',
                                     'https://5j0ilnnh1l.execute-api.us-west-2.amazonaws.com/tt')
    LAMBDA_X_API_KEY = os.getenv('LAMBDA_X_API_KEY', 'Rcp9a7US932wBZtp5Dd7P8rN5rY02UQF3qIw8iBO')

    SLACK_NOTIFICATION_URL = os.environ. \
        get('SLACK_NOTIFICATION_URL', 'https://hooks.slack.com/services/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')
    SERVICE_SLEEP_INTERVAL = os.environ.get('PROCESS_SLEEP_INTERVAL', 5)
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'aduro-data-dev')
    S3_IMAGE_PATH = os.environ.get('S3_IMAGE_PATH', f'images/{SOCIAL_NETWORK.lower()}')

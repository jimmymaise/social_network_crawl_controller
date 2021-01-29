import os


class SystemConfig:
    AM_BASE_URL = os.getenv('AM_BASE_URL', 'http://34.219.102.184:9099')

    MONGO_DB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
    MONGO_DB_PORT = os.environ.get('MONGODB_PORT', 27017)
    MONGO_DB_DATABASE_NAME = os.environ.get('MONGODB_DB', 'facebook')
    MONGO_DB_USERNAME = os.environ.get('MONGODB_USER')
    MONGO_DB_PASSWORD = os.environ.get('MONGODB_PASS')

    LAMBDA_BASE_URL = os.environ.get('LAMBDA_BASE_URL',
                                     'https://0t17hgh9td.execute-api.us-west-2.amazonaws.com/prod/')
    LAMBDA_X_API_KEY_POST_DETAIL = os.getenv('LAMBDA_X_API_KEY_POST_DETAIL', 'VNbGgsRzyF9NORS1HCAPt4d2TJsdNBFbrp4iUpM7')

    SLACK_NOTIFICATION_URL = os.environ. \
        get('SLACK_NOTIFICATION_URL', 'https://hooks.slack.com/services/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')
    SERVICE_SLEEP_INTERVAL = os.environ.get('PROCESS_SLEEP_INTERVAL', 5)

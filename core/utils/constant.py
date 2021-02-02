class Constant:
    AM_MAX_REQUEST = 3
    AM_DEFAULT_SLEEP_TIME = 3
    DEFAULT_LIMIT_NUM_ITEM = 10
    DEFAULT_MAXIMUM_DAYS_AFTER_TAKEN = 7
    SERVICE_CONFIG_FOLDER_NAME = 'service_config_samples'

    TOP_LEVEL_SCOPE = '__main__'
    LOG_FORMAT = '%(asctime)s - %(name)s: [%(levelname)s]: %(message)s'

    SOCIAL_TYPE_PROFILE = 'facebook'
    SOCIAL_TYPE_FAN_PAGE = 'facebook_page'
    SOCIAL_NETWORK_FACEBOOK = 'facebook'

    SERVICE_NAME_SEARCH_REPORT = 'search_report'
    SERVICE_NAME_COMMENT_REPORT = 'comment_report'

    COLLECTION_SERVICE_ERROR_NAME = 'collection_service_error_name'

    SLACK_DEFAULT_NOTIFICATION_FIELD = 'text'

    AM_API_GET_CRAWL_ACCOUNT_PATH = 'request'
    AM_API_UPDATE_CRAWL_ACCOUNT_PATH = 'account_update'

    DEFAULT_UNKNOWN_ERROR_CODE = 'error_unknown'

    MONGODB_FIND_TYPE_FIND_ONE = 'find_one'
    MONGODB_FIND_TYPE_FIND_MANY = 'find'

    REGEX_PATTERN_ONLY_NUMBER = '[0-9]+'
    REGEX_PATTERN_FB_USERNAME = '[aA-zZ0-9\.\-\_]+'

    TIME_ONE_MINUTE_TO_SECONDS = 60
    TIME_ONE_HOURS_TO_MINUTE = 60
    TIME_ONE_DAY_TO_HOURS = 24
    TIME_ONE_HOUR_TO_SECONDS = TIME_ONE_HOURS_TO_MINUTE * TIME_ONE_MINUTE_TO_SECONDS
    TIME_ONE_DAY_TO_SECONDS = TIME_ONE_DAY_TO_HOURS * TIME_ONE_HOUR_TO_SECONDS

    DEFAULT_TRANSFORM_ITEM_BATCH = 50

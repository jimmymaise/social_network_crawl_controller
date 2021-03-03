from core.utils.constant import Constant as CoreConstant


class Constant(CoreConstant):
    SOCIAL_TYPE_PROFILE = 'tiktok'
    SOCIAL_NETWORK_TIKTOK = 'tiktok'
    DEFAULT_PAGING_NUM_ITEM = 50
    SERVICE_NAME_SEARCH_REPORT = 'search_report'
    SERVICE_NAME_COMMENT_REPORT = 'comment_report'
    SERVICE_NAME_USER_COLLECTION = 'user_collection'

    COLLECTION_NAME_REPORT = 'reports'
    COLLECTION_NAME_KOL = 'kols'
    COLLECTION_NAME_USER = 'users'

    COLLECTION_NAME_MEDIA = 'medias'
    COLLECTION_NAME_COMMENT = 'comments'
    COLLECTION_NAME_POST_COMMENT = 'post_comments'

    COLLECTION_NAME_POST = 'posts'
    COLLECTION_SERVICE_ERROR_NAME = 'collection_service_error_name'

    SLACK_DEFAULT_NOTIFICATION_FIELD = 'text'

    LAMBDA_API_CRAWL_POST_DETAIL_PATH = 'post-details'
    LAMBDA_API_CRAWL_USER_DETAIL_PATH = 'user-details'

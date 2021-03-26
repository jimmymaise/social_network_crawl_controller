from core.utils.constant import Constant as CoreConstant


class Constant(CoreConstant):
    SOCIAL_TYPE_PROFILE = 'tiktok'
    SOCIAL_NETWORK_TIKTOK = 'tiktok'
    DEFAULT_PAGING_NUM_ITEM = 50
    POST_DEFAULT_PAGING_NUM_ITEM = 30

    SLACK_DEFAULT_NOTIFICATION_FIELD = 'text'

    LAMBDA_API_CRAWL_POST_DETAIL_PATH = 'post-details'
    LAMBDA_API_CRAWL_USER_DETAIL_PATH = 'user-details'
    LAMBDA_API_CRAWL_USER_POSTS_PATH = 'user-posts'

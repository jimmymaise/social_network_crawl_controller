from core.workflows.collect.utils.base_api_collect_utils import BaseApiCollectUtils
from social_networks.facebook.utils.constant import Constant
from social_networks.facebook.workflow.collect.utils.constant import APICollectConstant


class APICollectUtils(BaseApiCollectUtils):
    post_link_param_patterns = {
        'user_name': Constant.REGEX_PATTERN_FB_USERNAME,
        'user_id': Constant.REGEX_PATTERN_ONLY_NUMBER,
        'post_id': Constant.REGEX_PATTERN_ONLY_NUMBER,
        'album_id': Constant.REGEX_PATTERN_ONLY_NUMBER,
    }
    post_link_template_dict = APICollectConstant.POST_LINK_VALID_TEMPLATE_DICT

from core.workflows.collect.utils.base_api_collect_utils import BaseApiCollectUtils
from social_networks.instagram.utils.constant import Constant
from social_networks.instagram.workflow.collect.utils.constant import APICollectConstant


class APICollectUtils(BaseApiCollectUtils):
    post_link_param_patterns = {
        'shortcode': Constant.REGEX_PATTERN_IG_SHORT_CODE,
        'highlight_id': Constant.REGEX_PATTERN_ONLY_NUMBER,
    }
    post_link_template_dict = APICollectConstant.POST_LINK_VALID_TEMPLATE_DICT

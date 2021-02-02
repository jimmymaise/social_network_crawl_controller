import re


class BaseApiCollectUtils:
    @classmethod
    def is_validate_post_link_format(cls, post_link):
        for case, pattern_str in cls._post_link_valid_patterns().items():
            pattern = re.compile(f"^{pattern_str}$")
            if pattern.match(post_link):
                return True
        return False

    @classmethod
    def _post_link_valid_patterns(cls, post_link_template_dict, post_link_param_patterns):

        pattern_dict = {pattern_key: cls._make_url_pattern_from_url_template(pattern_url, **post_link_param_patterns)
                        for
                        pattern_key, pattern_url in
                        post_link_template_dict.items()}
        return pattern_dict

    @staticmethod
    def _make_url_pattern_from_url_template(url, **param_patterns):
        url = re.escape(url)
        url = url.replace('<', '{').replace('>', '}').format(**param_patterns)
        return url

import re


class APICollectUtils:
    @classmethod
    def is_validate_post_link_format(cls, post_link):
        for case, pattern_str in cls._post_link_valid_patterns().items():
            pattern = re.compile(f"^{pattern_str}$")
            if pattern.match(post_link):
                return True
        return False

    @staticmethod
    def _post_link_valid_patterns():
        user_name = '[a-z0-9]+'
        user_id = post_id = album_id = '[0-9]+'

        return {
            'profile_have_username': f'https://www\.facebook\.com/{user_name}/posts/{post_id}',
            'profile_not_have_username': f'https://www\.facebook\.com/permalink\.php?story_fbid={post_id}&id={user_id} ',
            'post_with_photo_album': f'https://www\.facebook\.com/{user_name}/photos/a\.{album_id}/{post_id}/',
            'live_stream_post': f'https://www\.facebook\.com/watch/live/?v={post_id}&ref=watch_permalink'

        }

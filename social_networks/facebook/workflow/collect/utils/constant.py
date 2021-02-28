class APICollectConstant:
    POST_LINK_VALID_TEMPLATE_DICT = {
        'profile_have_username': 'https://www.facebook.com/<user_name>/posts/<post_id>',
        'post_with_slash': 'https://www.facebook.com/<user_name>/\w+/<post_id>/',
        'profile_not_have_username': 'https://www.facebook.com/permalink.php?story_fbid=<post_id>&id=<user_id>',
        'post_with_photo_album': 'https://www.facebook.com/<user_name>/photos/a.<album_id>/<post_id>',
        'live_stream_post': 'https://www.facebook.com/watch/live/?v=<post_id>&ref=watch_permalink'
    }

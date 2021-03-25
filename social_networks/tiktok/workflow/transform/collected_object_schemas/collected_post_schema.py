from marshmallow import Schema, fields, EXCLUDE

from social_networks.tiktok.workflow.transform.collected_object_schemas.collected_user_schema import UserObjectSchema


class PostStats(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    digg_count = fields.Int(required=True)
    share_count = fields.Int(required=True)
    comment_count = fields.Int(required=True)
    play_count = fields.Int(required=True)


class PostVideo(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    _id = fields.Str(required=True)
    height = fields.Int()
    width = fields.Int()
    duration = fields.Int()
    ratio = fields.Str()
    cover = fields.Str()
    origin_cover = fields.Str()
    dynamic_cover = fields.Str()
    play_addr = fields.Str()
    download_addr = fields.Str()
    share_cover = fields.List(fields.Str())
    reflow_cover = fields.Str()


class PostMusic(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    _id = fields.Str(required=True)
    title = fields.Str()
    play_url = fields.Str()
    cover_thumb = fields.Str()
    cover_medium = fields.Str()
    cover_large = fields.Str()
    author_name = fields.Str()
    original = fields.Bool()
    duration = fields.Int()
    album = fields.Str()


class PostChallenge(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    _id = fields.Str(required=True)
    title = fields.Str()
    desc = fields.Str()
    profile_thumb = fields.Str()
    profile_medium = fields.Str()
    profile_larger = fields.Str()
    cover_thumb = fields.Str()
    cover_medium = fields.Str()
    cover_larger = fields.Str()
    is_commerce = fields.Bool()


class PostTextExtra(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    aweme_id = fields.Str()
    start = fields.Int()
    end = fields.Int()
    hashtag_name = fields.Str()
    hashtag_id = fields.Str()
    type = fields.Int()
    user_id = fields.Str()
    is_commerce = fields.Bool()
    user_unique_id = fields.Str()
    sec_uid = fields.Str()


class PostObjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = fields.Str(required=True)
    content = fields.Str(required=True)
    taken_at_timestamp = fields.Int(required=True)
    user_id = fields.Str(required=True)
    username = fields.Str(required=True)
    num_like = fields.Int(required=True)
    num_share = fields.Int(required=True)
    num_comment = fields.Int(required=True)
    num_view = fields.Int(required=True)
    display_url = fields.Str(required=True)
    video = fields.Nested(PostVideo)
    stats = fields.Nested(PostStats)
    music = fields.Nested(PostMusic)
    challenges = fields.List(fields.Nested(PostChallenge))
    original_item = fields.Bool()
    offical_item = fields.Bool()
    text_extra = fields.List(fields.Nested(PostTextExtra))
    secret = fields.Bool()
    for_friend = fields.Bool()
    digged = fields.Bool()
    item_comment_status = fields.Int()
    show_not_pass = fields.Bool()
    vl1 = fields.Bool()
    item_mute = fields.Bool()
    private_item = fields.Bool()
    duet_enabled = fields.Bool()
    stitch_enabled = fields.Bool()
    share_enabled = fields.Bool()
    is_ad = fields.Bool()
    author = fields.Nested(UserObjectSchema)

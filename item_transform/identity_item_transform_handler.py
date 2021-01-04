from item_transform.base_item_transform_handler import BaseItemTransformHandler
from .schema_objects.posts_object_schema import PostsObjectSchema
from .schema_objects.users_object_schema import UsersObjectSchema


class IdentityItemTransformHandler(BaseItemTransformHandler):
    def __init__(self):
        super().__init__()

    def process_item(self, load_item, collected_data):
        _user_data = self.get_users_data(collected_data)
        _post_data = self.get_posts_data(collected_data)

        # Validate schema
        user_data, error_user_data = self._validate_schema(_user_data, UsersObjectSchema)
        post_data, error_post_data = self._validate_schema(_post_data, PostsObjectSchema)

        # Build object to store
        user_objs = self.build_user_object(user_data, load_item)
        post_objs = self.build_user_object(post_data, load_item)

        return user_objs, post_objs

    @staticmethod
    def get_users_data(crawl_items):
        user_objs = {}

        return user_objs

    @staticmethod
    def get_posts_data(collected_data):
        post_objs = {}

        return post_objs

    @staticmethod
    def build_user_object(user_data, load_item):
        _user_objs = {}

        return _user_objs

    @staticmethod
    def build_post_object(post_data, load_item):
        _post_objs = {}

        return _post_objs


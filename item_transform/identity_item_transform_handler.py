from item_transform.base_item_transform_handler import BaseItemTransformHandler
from .schema_objects.posts_object_schema import PostsObjectSchema
from .schema_objects.users_object_schema import UsersObjectSchema


class IdentityItemTransformHandler(BaseItemTransformHandler):
    def __init__(self):
        super().__init__()

    def process_item(self, load_items, crawl_items):
        _user_data = self.get_users_data(crawl_items)
        _post_data = self.get_posts_data(crawl_items)

        # Validate schema
        user_data, error_user_data = self._validate_schema(_user_data, UsersObjectSchema)
        post_data, error_post_data = self._validate_schema(_post_data, PostsObjectSchema)

        # Build object to store
        user_objs = self.build_user_object(user_data, load_items)
        post_objs = self.build_user_object(post_data, load_items)

        return user_objs, post_objs

    @staticmethod
    def get_users_data(crawl_items):
        user_objs = {}

        return user_objs

    @staticmethod
    def get_posts_data(crawl_items):
        post_objs = {}

        return post_objs

    @staticmethod
    def build_user_object(user_data, load_items):
        _user_objs = {}

        return _user_objs

    @staticmethod
    def build_post_object(post_data, load_items):
        _post_objs = {}

        return _post_objs


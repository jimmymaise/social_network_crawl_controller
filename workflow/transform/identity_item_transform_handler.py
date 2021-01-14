from workflow.transform.base_item_transform_handler import BaseItemTransformHandler
from workflow.transform.schema_objects.posts_object_schema import PostObjectSchema
from workflow.transform.schema_objects.users_object_schema import UserObjectSchema


class IdentityItemTransformHandler(BaseItemTransformHandler):
    def __init__(self):
        super().__init__()

    def process_item(self, loaded_item, collected_data):
        user_data = self._extract_user_data_from_collected_data(collected_data)
        post_data = self._extract_post_data_from_collected_data(collected_data)

        # Validate schema
        user_data, error_user_data = self._validate_schema(user_data, UsersObjectSchema)
        post_data, error_post_data = self._validate_schema(post_data, PostsObjectSchema)

        if error_user_data and error_post_data:
            raise Exception('Invalid extracted data schema')

        # Build object to store
        user_obj = self._build_user_object(user_data, loaded_item)
        post_obj = self._build_user_object(post_data, loaded_item)

        return user_obj, post_obj

    @staticmethod
    def _extract_user_data_from_collected_data(collected_data):
        user_data = {}

        return user_data

    @staticmethod
    def _extract_post_data_from_collected_data(collected_data):
        post_data = {}

        return post_data

    @staticmethod
    def _build_user_object(user_data, loaded_item):
        user_objs = {}

        return user_objs

    @staticmethod
    def _build_post_object(post_data, loaded_item):
        post_objs = {}

        return post_objs

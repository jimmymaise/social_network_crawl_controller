from datetime import datetime

import more_itertools

from core.handlers.file_handler.s3_handler import S3Handler
from core.utils.exceptions import ErrorStoreFormat
from core.workflows.transform.base_item_transform_handler import BaseItemTransformHandler
from core.workflows.transform.stored_object.stored_object_builder import StoredObjectBuilder
from social_networks.tiktok.utils.constant import Constant
from social_networks.tiktok.workflow.transform.collected_object_schemas.collected_interaction_schema import \
    InteractionSchema


class PostsEngagementAnalyticsCollectionTransformHandler(BaseItemTransformHandler):
    def __init__(self, service_name):
        super().__init__(service_name)
        self.s3_handler = S3Handler()

    def process_item(self, loaded_item, collected_data):
        collected_data_chunks_iter = more_itertools.ichunked(collected_data, Constant.DEFAULT_TRANSFORM_ITEM_BATCH)
        for collected_data_chunk in collected_data_chunks_iter:
            user_objects = []

            # Save user
            for item in collected_data_chunk:
                user_objects.append(self._build_user_updated_object(collected_data=item))
            yield self._make_transformed_item(
                collection_name=Constant.COLLECTION_NAME_USER,
                updated_object_list=user_objects)

    def _build_user_updated_object(self, collected_data):
        data, collected_schema_error = self._validate_schema(data=collected_data, schema=InteractionSchema, dump=True)

        if collected_schema_error:
            raise ErrorStoreFormat(f'Schema error {str(collected_schema_error)}')

        user_stored_object_builder = StoredObjectBuilder()
        user_stored_object_builder.set_get_all_fields_from_collected_object('collected_user',
                                                                            excluded_fields=['_id', 'analyzed_post_to',
                                                                                             'analyzed_post_from']
                                                                            )

        user_stored_object = user_stored_object_builder.build(collected_user=data)
        last_time_analyze = int(datetime.now().timestamp())

        user_updated_object = self._make_updated_object(
            filter_={'_id': data['_id']},
            stored_object={
                'interaction': {
                    **user_stored_object,
                    'video': user_stored_object,
                    'analyzed_post_to': data['analyzed_post_to'],
                    'analyzed_post_from': data['analyzed_post_from'],
                    'last_time_analyze': last_time_analyze,
                }
            },
            upsert=False
        )

        return user_updated_object

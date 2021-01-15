import hashlib
from datetime import datetime

from core.utils.exceptions import ErrorStoreFormat
from workflow.transform.base_item_transform_handler import BaseItemTransformHandler
from workflow.transform.collected_object_schemas.collected_post_schema import PostObjectSchema
from workflow.transform.collected_object_schemas.collected_user_schema import UserObjectSchema
from workflow.transform.stored_object.stored_object_builder import StoredObjectBuilder


class PostReportTransformHandler(BaseItemTransformHandler):
    def __init__(self, service_name):
        super().__init__()
        self.service_name = service_name
        self.now = datetime.now()

    def process_item(self, loaded_item, collected_data):
        transformed_data = []
        _, collected_user_schema_error = self._validate_schema(data=collected_data['user'], schema=UserObjectSchema)
        _, collected_post_schema_error = self._validate_schema(data=collected_data['post'], schema=PostObjectSchema)

        if collected_post_schema_error:
            raise ErrorStoreFormat

        transformed_data.append(self._make_transformed_item(
            collection_name='post',
            updated_object_list=[self._build_post_updated_object(collected_data)])
        )
        transformed_data.append(self._make_transformed_item(
            collection_name='report',
            updated_object_list=[self._build_report_updated_object(collected_data, loaded_item)])
        )
        transformed_data.append(self._make_transformed_item(
            collection_name='media',
            updated_object_list=self._build_media_updated_objects(collected_data))
        )

        if not collected_user_schema_error:
            transformed_data.append(self._make_transformed_item(
                collection_name='kols',
                updated_object_list=self._build_kol_updated_object(collected_data))
            )
            transformed_data.append(self._make_transformed_item(
                collection_name='user',
                updated_object_list=self._build_user_updated_object(collected_data))
            )

        return transformed_data

    def _build_post_updated_object(self, collected_data):
        post_stored_object_builder = StoredObjectBuilder()
        post_stored_object_builder.set_get_all_fields_from_collected_object('collected_post',
                                                                            excluded_fields='full_picture')
        post_stored_object_builder.add_mapping('collected_post', {'_id': 'page_url'})
        post_stored_object_builder.add_mapping('collected_user', {'_id': 'user_id'})

        post_stored_object = post_stored_object_builder.build(collected_post=collected_data['post'],
                                                              collected_user=collected_data['user'])

        post_updated_object = self._make_updated_object(
            filter_={'_id': post_stored_object['_id']},
            stored_object=post_stored_object, )

        return post_updated_object

    def _build_user_updated_object(self, collected_data):
        user_stored_object_builder = StoredObjectBuilder()
        user_stored_object_builder.set_get_all_fields_from_collected_object('collected_user',
                                                                            excluded_fields='avatar')

        user_stored_object = user_stored_object_builder.build(collected_user=collected_data['user'])

        user_updated_object = self._make_updated_object(
            filter_={'_id': user_stored_object['_id']},
            stored_object=user_stored_object,
        )
        return user_updated_object

    def _build_kol_updated_object(self, collected_data):
        kol_stored_object_builder = StoredObjectBuilder()
        kol_stored_object_builder.add_mapping('collected_user', {'_id': 'user_id', 'username': 'username'})

        kol_stored_object = kol_stored_object_builder.build(collected_user=collected_data['user'])
        kol_updated_object = self._make_updated_object(
            filter_={'_id': kol_stored_object['_id']},
            stored_object=kol_stored_object,
        )

        return kol_updated_object

    def _build_media_updated_objects(self, collected_data) -> list:
        media_updated_objects = []
        media_stored_object_builder_by_post = StoredObjectBuilder()
        media_stored_object_builder_by_post.add_mapping('collected_post', {'full_picture': 'link'})
        media_stored_object = media_stored_object_builder_by_post.build(collected_post=collected_data['post'])
        media_stored_object['_id'] = hashlib.md5(media_stored_object['link'])
        media_updated_objects.append(self._make_updated_object(
            filter_=media_stored_object['_id'],
            stored_object=media_stored_object,
        ))
        if not collected_data['user'].get('avatar'):
            return media_stored_object

        media_stored_object_builder_by_user = StoredObjectBuilder()
        media_stored_object_builder_by_user.add_mapping('collected_user', {'avatar': 'link'})
        media_stored_object.append(media_stored_object_builder_by_user.build(collected_user=collected_data['user']))
        media_stored_object['_id'] = hashlib.md5(media_stored_object['link'])
        media_updated_objects.append(self._make_updated_object(
            filter_=media_stored_object['_id'],
            stored_object=media_stored_object,
        ))

        return media_updated_objects

    def _build_report_updated_object(self, collected_data, loaded_item):
        today_date = self.now.strftime("%Y-%m-%d")

        report_statuses = self._build_report_statuses_object()
        report_builder = StoredObjectBuilder()

        report_builder.add_mapping('history_report',
                                   {f'history_report.{today_date}': 'history_report'
                                    })
        report_builder.add_mapping('collected_post',
                                   {'_id': 'post_id'})
        report_builder.add_mapping('collected_user',
                                   {'username': 'username'})

        report_builder.set_get_all_fields_from_collected_object('report_statuses', None)

        report_stored_object = report_builder.build(
            report_statuses=report_statuses,
            collected_post=collected_data['post'],
            collected_user=collected_data['user']
        )
        report_stored_object['_id'] = loaded_item['_id']
        report_stored_object[f'history_report.{today_date}'] = self._build_history_report_object(collected_data)
        report_updated_object = self._make_updated_object(
            filter_={'_id': loaded_item['_id']},
            stored_object=report_stored_object,
        )
        return report_updated_object

    @staticmethod
    def _build_history_report_object(collected_data):
        today_report_history_builder = StoredObjectBuilder()
        today_report_history_builder.add_mapping('collected_post', {'num_reaction': 'num_reaction',
                                                                    'num_comment': 'num_comment',
                                                                    'num_share': 'num_share'
                                                                    })
        today_report_history = today_report_history_builder.build(collected_post=collected_data['post'])
        return today_report_history

    def _build_report_statuses_object(self):

        report_statuses_object = {
            f'{self.service_name}_status': {'status': 'success',
                                            'latest_updated_time': int(self.now.timestamp())
                                            },
            'response_server.is_update_report': False,
            'response_server.last_time_update': 0,
        }
        return report_statuses_object

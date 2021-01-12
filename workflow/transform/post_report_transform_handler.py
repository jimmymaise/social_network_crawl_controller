import copy

from workflow.transform.base_item_transform_handler import BaseItemTransformHandler
from workflow.transform.extract_stored.store_object_builder import StoredObjectBuilder


class PostReportTransformHandler(BaseItemTransformHandler):
    def __init__(self):
        super().__init__()

    def process_item(self, loaded_item, collected_data):
        # todo validate schema of collected_data ???

        post_stored_object = self._build_post_stored_object(collected_data)
        user_stored_object = self._build_user_stored_object(collected_data)
        kol_stored_object = self._build_kol_stored_object(collected_data)
        media_stored_objects = self._build_media_stored_objects(collected_data)
        report_stored_object = self._build_report_stored_object(collected_data, loaded_item)

        # todo validate schema of stored object

        return post_stored_object, user_stored_object, kol_stored_object, media_stored_objects, report_stored_object

    @staticmethod
    def _build_post_stored_object(collected_data):
        post_stored_object_builder = StoredObjectBuilder()
        post_stored_object_builder.set_get_all_fields_from_collected_object('collected_post',
                                                                            excluded_fields='full_picture')
        post_stored_object_builder.add_mapping('collected_post', {'_id': 'page_url'})
        post_stored_object_builder.add_mapping('collected_user', {'_id': 'user_id'})

        post_stored_object = post_stored_object_builder.build(collected_post=collected_data['post'],
                                                              collected_user=collected_data['user'])

        return post_stored_object

    @staticmethod
    def _build_user_stored_object(collected_data):
        user_stored_object_builder = StoredObjectBuilder()
        user_stored_object_builder.set_get_all_fields_from_collected_object('collected_user',
                                                                            excluded_fields='avatar')

        user_stored_object = user_stored_object_builder.build(collected_user=collected_data['user'])
        return user_stored_object

    @staticmethod
    def _build_kol_stored_object(collected_data):
        kol_stored_object_builder = StoredObjectBuilder()
        kol_stored_object_builder.add_mapping('collected_user', {'_id': 'user_id', 'username': 'username'})

        kol_stored_object = kol_stored_object_builder.build(collected_user=collected_data['user'])
        return kol_stored_object

    @staticmethod
    def _build_media_stored_objects(collected_data) -> list:
        media_stored_objects = []
        media_stored_object_builder_by_user = StoredObjectBuilder()
        media_stored_object_builder_by_user.add_mapping('collected_user', {'avatar': 'link'})
        media_stored_objects.append(media_stored_object_builder_by_user.build(collected_user=collected_data['user']))

        media_stored_object_builder_by_post = StoredObjectBuilder()
        media_stored_object_builder_by_post.add_mapping('collected_post', {'full_picture': 'link'})
        media_stored_objects.append(media_stored_object_builder_by_post.build(collected_post=collected_data['post']))

        return media_stored_objects

    @classmethod
    def _build_report_stored_object(cls, collected_data, loaded_item):
        history_report = cls._build_history_report_object(collected_data, loaded_item)
        report_statuses = cls._build_report_statuses_object(collected_data, loaded_item)
        report_builder = StoredObjectBuilder()

        report_builder.add_mapping('history_report', {'history_report': 'history_report'
                                                      })
        report_builder.add_mapping('collected_post', {'_id': 'post_id'})
        report_builder.add_mapping('collected_user', {'username': 'username'})

        report_builder.set_get_all_fields_from_collected_object('report_statuses', None)

        report_stored_object = report_builder.build(history_report=history_report,
                                                    report_statuses=report_statuses,
                                                    collected_post=collected_data['post'],
                                                    collected_user=collected_data['user']
                                                    )
        return report_stored_object

    @staticmethod
    def _build_history_report_object(collected_data, loaded_item):
        today_date = '2020-01-12'  # todo remove hardcode here
        today_report_history_builder = StoredObjectBuilder()
        today_report_history_builder.add_mapping('collected_post', {'num_reaction': 'num_reaction',
                                                                    'num_comment': 'num_comment',
                                                                    'num_share': 'num_share'
                                                                    })
        today_report_history = today_report_history_builder.build(collected_post=collected_data['post'])
        history_report_object = copy.deepcopy(loaded_item['history_report']).append(
            {'today_date': today_report_history})
        return history_report_object

    @staticmethod
    def _build_report_statuses_object(collected_data, loaded_item):
        # todo implement it
        report_statuses_object = {
            'status': None,
            'last_time_checking': None,
            'response_server': None,
            'tracking_status': None,
        }
        return report_statuses_object

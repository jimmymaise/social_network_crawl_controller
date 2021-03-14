import json

from core.handlers.db_handler.collection_lookup_handler import CollectionLookupHandler
from core.handlers.queue_handler.sqs_handler import SQSHandler
from core.utils.constant import Constant


class BaseSyncDataHandler:
    def __init__(self, db_connection):
        self.sqs_handler = SQSHandler()
        self.db_connection = db_connection

    def user_data_sync(self, find_user_query, queue_name):
        user_collection_lookup_handler = CollectionLookupHandler(collection_name=Constant.COLLECTION_NAME_USER,
                                                                 db_connection=self.db_connection)
        user_collection_lookup_handler.add_lookup_field(
            lookup_field_name='avatar',
            collection_lookup=Constant.COLLECTION_NAME_MEDIA,
            field_name_local='avatar',
            field_name_foreign='_id',
            field_name_return='link')

        user_collection_lookup_handler.add_lookup_field(
            lookup_field_name='country_code',
            collection_lookup=Constant.COLLECTION_NAME_KOL,
            field_name_local='username',
            field_name_foreign='username',
            field_name_return='country_code')
        user_collection_lookup_handler.match(
            find_user_query
        )
        user_sync_data = user_collection_lookup_handler.query()[0]
        self.sqs_handler.send_sqs_message(message_body=json.dumps(user_sync_data),
                                          queue_name=queue_name)
        return user_sync_data

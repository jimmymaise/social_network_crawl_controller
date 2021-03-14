import json

from core.workflows.sync_data.base_sync_data_handler import BaseSyncDataHandler


class SyncDataHandler(BaseSyncDataHandler):
    def __init__(self, db_connection):
        super().__init__(db_connection)

    def user_post_list_request(self, user_id, username, sec_uid, queue_name):
        request_message = {
            'user_id': user_id,
            'username': username,
            'sec_uid': sec_uid,
            'queue_name': queue_name
        }
        self.sqs_handler.send_sqs_message(message_body=json.dumps(request_message),
                                          queue_name=queue_name)

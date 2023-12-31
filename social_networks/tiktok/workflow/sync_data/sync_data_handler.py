import json

from core.workflows.sync_data.base_sync_data_handler import BaseSyncDataHandler
from social_networks.tiktok.utils.constant import Constant


class SyncDataHandler(BaseSyncDataHandler):
    def __init__(self, db_connection):
        super().__init__(db_connection, Constant.SOCIAL_NETWORK_TIKTOK)

    def user_post_list_request(self, hiip_user_id, user_id, username, country_code, sec_uid, queue_name):
        request_message = {
            'country_code': country_code,
            'hiip_user_id': hiip_user_id,
            'social_user_id': user_id,
            'social_user_name': username,
            'sec_uid': sec_uid,
            'service_name': 'post_list_collection',
            'social_type': self.social_type
        }
        self.sqs_handler.send_sqs_message(message_body=json.dumps(request_message),
                                          queue_name=queue_name)

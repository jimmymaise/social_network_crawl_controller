import json


class OnDemandHandler:
    def __init__(self, event, context):
        self.event = event
        self.context = context
        self.message = self._get_message_from_event()

    def _get_message_from_event(self):
        if len(self.event['Records']) > 1:
            raise NotImplementedError(f'Currently, we just support only one message per time {json.dumps(self.event)}')
        self.message = self.event['Records'][0]['body']

        if isinstance(self.message, str):
            try:
                self.message = json.loads(self.message)
            except Exception as e:
                raise Exception(f'Error to load message {self.message}. Exception {e}')
        return self.message

    def get_service_name_social_network_from_event(self):
        service_name, social_network = self.message['service_name'], self.message['social_type']
        return service_name, social_network

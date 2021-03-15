import json


class OnDemandHandler:
    def __init__(self, event, context):
        self.event = event
        self.context = context
        self.message = self._get_message_from_event()

    def _get_message_from_event(self):
        if len(self.event['Records']) > 1:
            raise NotImplementedError('Currently, we just support only one message per time')
        message_str = self.event['Records'][0]
        self.message = json.loads(message_str)
        return self.message

    def get_service_name_social_network_from_event(self):
        service_name, social_network = self.message['service_name'], self.message['social_type']
        return service_name, social_network

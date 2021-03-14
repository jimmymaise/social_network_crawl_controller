import os
from enum import Enum

from config.service_config import ServiceConfigs
from config.system_config import SystemConfig
from core.handlers.on_demand_handler.on_demand_handler import OnDemandHandler
from social_networks.facebook.services.service_factory import ServiceFactory as FacebookServiceFactory
from social_networks.instagram.services.service_factory import ServiceFactory as InstagramServiceFactory
from social_networks.tiktok.services.service_factory import ServiceFactory as TiktokServiceFactory


class SocialNetworkServiceFactory(Enum):
    FACEBOOK = FacebookServiceFactory
    INSTAGRAM = InstagramServiceFactory
    TIKTOK = TiktokServiceFactory


class ServicesRunner:
    def __init__(self):
        self.system_config = SystemConfig.get_system_config()
        self.service_config = ServiceConfigs.get_service_config()

    def run(self):
        service_name, social_network = self.service_config['SERVICE_NAME'], self.system_config.SOCIAL_NETWORK
        service_factory = getattr(SocialNetworkServiceFactory, social_network).value
        service = service_factory.create_service(service_name=service_name,
                                                 service_config=self.service_config)

        service.start()


class ServiceOnDemandRunner:
    def __init__(self, event, context):
        os.environ['LAMBDA'] = 'LAMBDA'
        self.on_demand_handler = OnDemandHandler(event=event, context=context)
        service_name, social_network = self.on_demand_handler.get_service_name_social_network_from_event()
        self.system_config = SystemConfig.get_system_config(social_network)

    def run(self):
        service_name, social_network = self.on_demand_handler.get_service_name_social_network_from_event()
        service_factory = getattr(SocialNetworkServiceFactory, social_network.upper()).value

        service = service_factory.create_service(service_name=service_name,
                                                 service_config=None,
                                                 on_demand_handler=self.on_demand_handler
                                                 )
        service.start()


def lambda_handler(event, context):
    return ServiceOnDemandRunner(event, context).run()


if __name__ == '__main__':
    # ServicesRunner().run()
    lambda_handler({
        'Records': [{'social_type': 'tiktok',
                     'social_name': 'cuti',
                     'social_app_id': '123',
                     'social_user_name': 'fandom',
                     'country_code': 'vi',
                     'hiip_user_id': 1234,

                     'taken_at_timestamp': 11,
                     'service_name': 'user_collection', }]}, {})

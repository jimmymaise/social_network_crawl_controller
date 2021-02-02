from enum import Enum

from config.service_config import ServiceConfigs
from config.system_config import SystemConfig
from social_networks.facebook.services.service_factory import ServiceFactory as FacebookServiceFactory


class SocialNetworkServiceFactory(Enum):
    FACEBOOK = FacebookServiceFactory


class ServicesRunner:
    def __init__(self):
        self.system_config = SystemConfig
        self.service_config = ServiceConfigs.get_service_config()

    def run(self):
        service_name, social_network = self.service_config['SERVICE_NAME'], self.system_config.SOCIAL_NETWORK
        service_factory = getattr(SocialNetworkServiceFactory, social_network).value
        service = service_factory.create_service(service_name=service_name,
                                                 service_config=self.service_config)

        service.start()


ServicesRunner().run()

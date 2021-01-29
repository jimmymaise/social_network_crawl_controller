from config.service_config import ServiceConfigs
from config.system_config import SystemConfig
from services.service_factory import ServiceFactory


class ServicesRunner:
    def __init__(self):
        self.system_config = SystemConfig
        self.service_config = ServiceConfigs.get_service_config()

    def run(self):
        service_name, service_config = self.service_config['SERVICE_NAME'], self.service_config
        service = ServiceFactory.create_service(service_name=service_name,
                                                service_config=service_config)
        service.start()


ServicesRunner().run()

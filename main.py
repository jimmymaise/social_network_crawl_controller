from config.service_configs import ServiceConfigs
from config.system_config import SystemConfig
from services.service_factory import ServiceFactory


class ServicesRunner:
    def __init__(self):
        self.system_config = SystemConfig
        self.service_configs = ServiceConfigs.get_service_configs()

    def run(self):
        for service_name, service_config in self.service_configs['SERVICES'].items():
            service = ServiceFactory.create_service(service_name=service_name,
                                                    service_config=service_config)
            service.start()


ServicesRunner().run()

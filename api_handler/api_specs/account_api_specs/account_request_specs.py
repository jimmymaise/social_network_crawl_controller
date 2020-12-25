class AccountRequestSpecs:
    api_type: str = 'GET'
    api_body: dict

    def set_api_body(self, social_network, service, country):
        self.api_body = {
                "social_network": social_network.upper() if isinstance(social_network, str) else "ALL",
                "service_name": service.upper() if isinstance(service, str) else "ALL",
                "country": country.upper() if isinstance(country, str) else "ALL",
            }

    def get_payload(self):
        return {
            'api_type': self.api_type,
            'api_body': self.api_body
        }

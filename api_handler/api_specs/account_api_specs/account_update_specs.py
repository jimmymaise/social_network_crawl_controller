class AccountUpdateSpecs:
    api_type: str = 'UPDATE_STATUS'
    api_body: dict

    def set_api_body(self, social_network, account_id, status_code, message=None):
        self.api_body = {
                "social_network": social_network.upper(),
                "account_ID": account_id,
                "data": {
                    "status_code": status_code,
                    "message": message
                }
            }

    def get_payload(self):
        return {
            'api_type': self.api_type,
            'api_body': self.api_body
        }
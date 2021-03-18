import json

from main import lambda_handler

if __name__ == '__main__':
    message = {"social_type": "tiktok",
               "social_name": "cuti",
               "social_user_name": "lebong95",
               "country_code": "vi",
               "hiip_user_id": 1234,
               "sec_uid": 'MS4wLjABAAAAL7fKextCmJnaMSNxmPYnsxqfXoYgJs9r8fd7viWLA-0hSxrLM8wFPtaKEtWcI51R',
               "taken_at_timestamp": 11,
               "service_name": "post_list_collection"}
    data = {"Records": [{'body': json.dumps(message)}]}
    lambda_handler(data, {})
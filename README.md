
How to run this repos:
1. Set environment variable like the file config/system_config.py.

2. If you are running service in local environment, you need to set environment variable ENV = 'local' and set DEFAULT_SERVICE_LOCAL = the name of service you want to run. 
Doing so, it will get the service_config variable in social_networks/`name_of_social_network`/service_config_samples/`name_of_service.json`
Without setting ENV ='local',  it will get  the service_config variable in the environment variable SERVICE_CONFIG (the json schema is the same service_config_sample but it need to be base 64 encoded)

3. Run main.py file

Note: 

- It may load 0 item if no documents in your report table meets filter conditions, check social_networks/`name_of_social_network`/workflow/load,ing/query/report_query.py. We may need to change taken_at_timestamp, country_code in a document to meet filter query.

- It may have issue when connect to account_manager service. In order to work arround, add sample data for account_info.
For example, in socail_networks/instagram/workflow/collect/api_collect_handler.py, inside func get_comments_from_lambda, we can set below data right after the line 
`account_info, account_id = self.crawl_account_handler.get_account_id_token()`

           
		 
	account_info = {
		 "account_id": "accountID_001",
            "query_hash": "bc3296d1ce80a24b1b6e40b1e72903f5",
            "info": {
                "csrftoken": "yvkUNvit4ykNTUqjtDNuYTHVsODBy8pT",
                "datr": "3Wo_Xw2nKCBXzdsCXJspwrnz",
                "ds_user_id": "4026520510",
                "ig_cb": "1",
                "ig_did": "7ECD68B5-8FD8-48D3-AAEA-E2A73A30E568",
                "mid": "XEiL-gALAAH50f_Tc7Kyv0tMXM5C",
                "rur": "FRC",
                "sessionid": "4026520510%3AvrZU5wdcPUkHOZ%3A17",
                "shbid": "14922",
                "shbts": "1610507777.3079073"
            }
        }


Userful links:
1. Docker database for dev env: https://gitlab.com/hiip-bigdata/dev-enviroment
2. Collection Service Architect: https://docs.google.com/spreadsheets/d/1ohwvANLR1Kt-edxBajDPlTAfnn4p3hzZBVteqYsO28Q/edit#gid=0







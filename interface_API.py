import requests
import json
import base64
import datetime

class interface_API():
    def __init__(self):
        self.bearer_token = self.bearerToken()
        self.tokentime = datetime.datetime.now().timestamp()
        

    def token_check(self):
        t_now = datetime.datetime.now().timestamp()
        if (t_now - self.tokentime) > 25:
            self.bearer_token = self.bearerToken()
            print(self.bearer_token)


    def bearerToken(self):
        #--- App details from developer cockpit
        CLIENT_ID = "iiotuxpc-testdm-v1.0.0"
        CLIENT_SECRET = "UvwnNgdc8Y0KsE7IZSFy2Jp28kQGzAd0fEHXcDOWbIX"
        APP_NAME = "testdm"
        APP_VERSION = "v1.0.0"
        HOST_TENANT = "iiotuxpc"
        USER_TENANT = "iiotuxpc"
        credential_create_time = "23/02/2023::18:53"

        #--- generate access token
        id = CLIENT_ID
        secret = CLIENT_SECRET
        encode_msg = id + ":" + secret
        token = base64.b64encode(encode_msg.encode("utf-8")).decode("utf-8")
        url = "https://gateway.eu1.mindsphere.io/api/technicaltokenmanager/v3/oauth/token"

        payload = json.dumps({
        "grant_type": "client_credentials",
        "appName": APP_NAME,
        "appVersion": APP_VERSION,
        "hostTenant": HOST_TENANT,
        "userTenant": USER_TENANT
        })
        headers = {
        'X-SPACE-AUTH-KEY': "Basic " + token,
        'Content-Type': 'application/json'
        }

        token_response = requests.request("POST", url, headers=headers, data=payload)
        # print(token_response.text)
        bearer_token = json.loads(token_response.text)["access_token"]
        return(bearer_token)

    def get_assetid(self,asset_name,bearer_token):
        #--- get list of assets
        url = "https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets"
        payload={}
        headers = {
        'Authorization': 'Bearer ' + bearer_token
        }
        assets_list_response = requests.request("GET", url, headers=headers, data=payload)  # GET API call for assets_list
        assets_list=json.loads(assets_list_response.text)
        assets_count = assets_list["page"]["totalElements"]     # total number of assets available
        
        #--- find the asset_name and the corresponding ID in the assets_list
        for ii in range(0,assets_count):
            if assets_list["_embedded"]["assets"][ii]["name"] == asset_name:
                asset_Id = assets_list["_embedded"]["assets"][ii]["assetId"]
                # print(asset_name,asset_Id)
                break
        else: print("Error:\n\tAsset not found in the assets list.\n\tVerify the accuracy of asset name and the assets list. Asset name is case sensitive.")
        return(asset_Id)

    def get_timeseries(self,asset_Id, aspect_name, from_time, to_time,bearer_token):
        
        data_condition = "?from=" + from_time + "&to=" + to_time    # query condition with from and to time period
        end_point = "iottimeseries/v3/timeseries/" + asset_Id + "/" + aspect_name + data_condition
        base_url = "https://gateway.eu1.mindsphere.io/api/"
        url = base_url + end_point

        payload={}
        headers = {
        'Authorization': 'Bearer ' + bearer_token
        }

        time_series_response = requests.request("GET", url, headers=headers, data=payload)  # GET API call
        print(time_series_response.text)
        time_series=json.loads(time_series_response.text)
        return(time_series)
    

    def put_timeseries(self,asset_id, aspect_name, payload,bearer_token):
                
        end_point = "iottimeseries/v3/timeseries/" + asset_id + "/" + aspect_name
        base_url = "https://gateway.eu1.mindsphere.io/api/"
        url = base_url + end_point

        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + bearer_token
        }

        response = requests.request("PUT", url, headers=headers, data=payload)  # PUT API call
        if not response.text:
            print("Data PUT successfully.")
        else:print("Error:\n\t",response.text)

    def indicator(self, logic, input, asset_id = "7da127f5a566408db16e0aeace5181e9"):
        aspect_name = "validation_indicator"
        payload = json.dumps([
            {
            "_time" : datetime.datetime.utcnow().isoformat() + 'Z',
            "logic" : logic,
            "input" : input
            }
        ])
        self.token_check()
        self.put_timeseries(payload = payload, asset_id = asset_id, aspect_name=aspect_name, bearer_token=self.bearer_token)

    def station_status(self, station_1, station_2, station_3, station_4, station_5, asset_id = "7da127f5a566408db16e0aeace5181e9"):
        aspect_name = "station_status"
        payload = json.dumps([
            {
            "_time" : datetime.datetime.utcnow().isoformat() + 'Z',
            "station_1" : station_1,
            "station_2" : station_2,
            "station_3" : station_3,
            "station_4" : station_4,
            "station_5" : station_5
            }
        ])
        self.token_check()
        self.put_timeseries(payload = payload, asset_id = asset_id, aspect_name=aspect_name, bearer_token=self.bearer_token)

    def queue_status(self, queue_1, queue_2, queue_3, queue_4, queue_5, asset_id = "7da127f5a566408db16e0aeace5181e9"):
        aspect_name = "queue_status"
        payload = json.dumps([
            {
            "_time" : datetime.datetime.utcnow().isoformat() + 'Z',
            "queue_1" : queue_1,
            "queue_2" : queue_2,
            "queue_3" : queue_3,
            "queue_4" : queue_4,
            "queue_5" : queue_5
            }
        ])
        self.token_check()
        self.put_timeseries(payload = payload, asset_id = asset_id, aspect_name=aspect_name, bearer_token=self.bearer_token)

    def RCT_server(self, part_id, path_1, path_2, queue_id, asset_id = "f018a3e7cc4343efa5cc9eced3cc11d5"):
        aspect_name = "station_status"
        payload = json.dumps([
            {
            "_time" : datetime.datetime.utcnow().isoformat() + 'Z',
            "part_id" : part_id,
            "path_1" : path_1,
            "path_2" : path_2,
            "queue_id" : queue_id
            }
        ])
        self.token_check()
        self.put_timeseries(payload = payload, asset_id = asset_id, aspect_name=aspect_name, bearer_token=self.bearer_token)


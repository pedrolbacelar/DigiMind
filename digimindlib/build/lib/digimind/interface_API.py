import requests
import json
import base64
import datetime

class interfaceAPI():
    def __init__(self, asset_name = "DigiMind"):
        self.asset_name = asset_name
        self.bearer_token_flag = False
        self.asset_id_flag = False
        self.bearer_token = self.bearerToken()
        self.tokentime = datetime.datetime.now().timestamp()
        if self.bearer_token_flag is True:
            self.asset_id = self.get_assetid()
        if self.bearer_token_flag and self.asset_id_flag is True:
            print(f"API object created for '{self.asset_name}'.")
        else:
            print(f"\nAPI object failed to create. Check whether '{self.asset_name}' is the correct asset name.\n\n")

    def token_check(self):
        t_now = datetime.datetime.now().timestamp()
        if (t_now - self.tokentime) > 1700:
            self.bearer_token = self.bearerToken()  #--- renewing bearer token as it expires in 1799 seconds
            self.tokentime = t_now      #--- updating the time when the next token was created.
            print(self.bearer_token)


    def bearerToken(self):
        
        #--- App details from developer cockpit
        APP_NAME = "cannon"
        APP_VERSION = "v1.0.0"
        HOST_TENANT = "mswitops"
        USER_TENANT = "mswitpro"
        credential_create_time = "created by organizer"

        #--- access token provided by the organizer
        token = "bXN3aXRvcHMtY2Fubm9uLXYxLjAuMC0xMzc4NTgwMjQ6U0RxUFpabjl0YkJodUM2V0VwUGFONEdZbzJFN2k0dWpBcEJTTlUzOUJ5QQ=="

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
        if "access_token" in json.loads(token_response.text):
                bearer_token = json.loads(token_response.text)["access_token"]
                self.bearer_token_flag = True
                return(bearer_token)
        else:
            print("\n\nBearer token failed to generate.\nTrying to generate bearer token again ......\n...\n...")
            token_response = requests.request("POST", url, headers=headers, data=payload)
            if "access_token" in json.loads(token_response.text):
                bearer_token = json.loads(token_response.text)["access_token"]
                self.bearer_token_flag = True
                return(bearer_token)
            else:
                print("\n\nBearer token failed to generate. Please check the internet connectivity and the client credentials.\n\n")


    def get_assetid(self):
        #--- get list of assets
        url = "https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets"
        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.bearer_token
        }
        assets_list_response = requests.request("GET", url, headers=headers, data=payload)  # GET API call for assets_list
        assets_list=json.loads(assets_list_response.text)
        assets_count = assets_list["page"]["totalElements"]     # total number of assets available
        
        try:
            #--- find the asset_name and the corresponding ID in the assets_list
            for ii in range(0,assets_count):
                if assets_list["_embedded"]["assets"][ii]["name"] == self.asset_name:
                    asset_id = assets_list["_embedded"]["assets"][ii]["assetId"]
                    # print(asset_name,asset_Id)
                    self.asset_id_flag = True
                    break
            else:
                print("Error:\n\tAsset not found in the assets list.\n\tVerify the accuracy of asset name and the assets list. Asset name is case sensitive.")

            return(asset_id)
        except IndexError:
            print("Error:\n\tAsset not found in the assets list.\n\tVerify the accuracy of asset name and the assets list. Asset name is case sensitive.")

    def get_timeseries(self, aspect_name, from_time, to_time):
        
        data_condition = "?from=" + from_time + "&to=" + to_time    # query condition with from and to time period
        end_point = "iottimeseries/v3/timeseries/" + self.asset_id + "/" + aspect_name + data_condition
        base_url = "https://gateway.eu1.mindsphere.io/api/"
        url = base_url + end_point

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.bearer_token
        }

        time_series_response = requests.request("GET", url, headers=headers, data=payload)  # GET API call
        print(time_series_response.text)
        time_series=json.loads(time_series_response.text)
        return(time_series)
    

    def put_timeseries(self, aspect_name, payload):
                
        end_point = "iottimeseries/v3/timeseries/" + self.asset_id + "/" + aspect_name
        base_url = "https://gateway.eu1.mindsphere.io/api/"
        url = base_url + end_point

        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + self.bearer_token
        }

        response = requests.request("PUT", url, headers=headers, data=payload)  # PUT API call
        if not response.text:
            print(f"Following data was PUT successfully to '{aspect_name}' aspect: {payload}")
        else:
            print(f"Error during '{aspect_name}' PUT method:\n\t",response.text)
            print("Trying again ...................\n....\n....")
            response2 = requests.request("PUT", url, headers=headers, data=payload)  # PUT API call
            if not response2.text:
                print(f"Following data was PUT successfully to '{aspect_name}' aspect: {payload} in the second attempt.")
            else:
                print(f"\nPUT method failed for '{aspect_name}' again. Attention required !!!")
                print("Error:\n\t",response2.text)

    #--- write validation indicator [Mean_Absolute_Error,Prediction_Reliability] = [float, float]
    def Indicator(self, data):
        aspect_name = "Indicator"
        payload = json.dumps([
            {
            "_time" : datetime.datetime.utcnow().isoformat() + 'Z',
            "Mean_Absolute_Error" : data[0],
            "Prediction_Reliability" : data[1]
            }
        ])
        self.token_check()
        self.put_timeseries(payload = payload, aspect_name=aspect_name)

    #--- write station_status [Part_ID, Remaining_Cycle_Time] = [string, int]
    def RCT(self, data):
        aspect_name = "RCT"
        payload = json.dumps([
            {
            "_time" : datetime.datetime.utcnow().isoformat() + 'Z',
            "Part_ID" : data[0],
            "Remaining_Cycle_Time" : data[1]
            }
        ])
        self.token_check()
        self.put_timeseries(payload = payload, aspect_name=aspect_name)

    #--- write queue_status [Position, Queue_1, Queue_2, Queue_3, Queue_4] = [int, int, int, int, int]
    def Zone(self, data):
        aspect_name = "Zone"
        payload = json.dumps([
            {
            "_time" : datetime.datetime.utcnow().isoformat() + 'Z',
            "Position" : data[0],
            "Queue_1" : data[1],
            "Queue_2" : data[2],
            "Queue_3" : data[3],
            "Queue_4" : data[4],
            "Queue_5" : data[5]
            }
        ])
        self.token_check()
        self.put_timeseries(payload = payload, aspect_name=aspect_name)


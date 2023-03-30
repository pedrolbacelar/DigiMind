## Access token (bearer token)
expires in 1799 seconds or less than 30 minutes.
### with postman
post
url: https://gateway.eu1.mindsphere.io/api/technicaltokenmanager/v3/oauth/token
Auhtorisation: No Auth
Header:
- key: X-SPACE-AUTH-KEY; Value: Basic <base64 encoded client details>
- key: Content-Type; Value: application/json
- body: {"grant_type": "client_credentials","appName": "<app internal name>","appVersion": "<version with v>","hostTenant": "<tenant name>","userTenant": "<tenant name>"}
X-SPACE-AUTH-KEY: it is basically client id and client secret encoded with base64. It can be done at base64encode.org by specifying <clientid>:<client-secret> and clicking encode.

### with Python
X-SPACE-AUTH key can be generated with base64 encoding as mentioned above
```python
import requests
import json

url = "https://gateway.eu1.mindsphere.io/api/technicaltokenmanager/v3/oauth/token"

payload = json.dumps({
  "grant_type": "client_credentials",
  "appName": "testdm",
  "appVersion": "v1.0.0",
  "hostTenant": "iiotuxpc",
  "userTenant": "iiotuxpc"
})
headers = {
  'X-SPACE-AUTH-KEY': 'Basic aWlvdHV4cGMtdGVzdGRtLXYxLjAuMDpVdnduTmdkYzhZMEtzRTdJWlNGeTJKcDI4a1FHekFkMGZFSFhjRE9XYklY',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```
for generating base64 encoding and X-SPACE-AUTH-KEY
```python
import json
import base64

id = CLIENT_ID
secret = CLIENT_SECRET
encode_msg = id + ":" + secret

token = base64.b64encode(encode_msg.encode("utf-8")).decode("utf-8")

X-SPACE-AUTH-KEY = "Basic " + token

```

## get assets
url = https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets
Auhtorisation: Bearer token: bearer token generated

```python
import requests

url = "https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets"

payload={}
headers = {
  'Authorization': 'Bearer ' + bearer_token
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```
example:
```json
{"_embedded":{"assets":[{"assetId":"343a6a61f5ef48c899b13f9c1be45b07","tenantId":"iiotuxpc","name":"iiotuxpc","etag":0,"externalId":null,"t2Tenant":null,"subTenant":null,"description":"Root Asset for iiotuxpc tenant","timezone":"Europe/Berlin","twinType":"performance","parentId":"","typeId":"core.basicenterprise","location":null,"fileAssignments":[],"variables":[{"name":"tenantFlag","value":"true"}],"aspects":[],"locks":[],"deleted":null,"sharing":{"modes":[]},"_links":{"self":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/343a6a61f5ef48c899b13f9c1be45b07"},"aspects":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/343a6a61f5ef48c899b13f9c1be45b07/aspects"},"variables":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/343a6a61f5ef48c899b13f9c1be45b07/variables"},"location":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/343a6a61f5ef48c899b13f9c1be45b07/location"},"children":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets?filter=%7B%22parentId%22:%22343a6a61f5ef48c899b13f9c1be45b07%22%7D"}}},{"assetId":"60bf86d1d051416f853b1e22f3714b8c","tenantId":"iiotuxpc","name":"machine","etag":0,"externalId":"","t2Tenant":null,"subTenant":null,"description":"","timezone":"Europe/Berlin","twinType":"performance","parentId":"343a6a61f5ef48c899b13f9c1be45b07","typeId":"iiotuxpc.station","location":null,"fileAssignments":[],"variables":[],"aspects":[{"name":"connectivityStatus","variables":[{"name":"connected","value":"false"}]}],"locks":[],"deleted":null,"sharing":{"modes":[]},"_links":{"self":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/60bf86d1d051416f853b1e22f3714b8c"},"aspects":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/60bf86d1d051416f853b1e22f3714b8c/aspects"},"variables":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/60bf86d1d051416f853b1e22f3714b8c/variables"},"location":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/60bf86d1d051416f853b1e22f3714b8c/location"},"parent":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/343a6a61f5ef48c899b13f9c1be45b07"}}},{"assetId":"574fbc1ab7964fa3a6acf1173707a256","tenantId":"iiotuxpc","name":"MobilePhone","etag":11,"externalId":null,"t2Tenant":null,"subTenant":null,"description":"Digital representation of a mobile phone of both types, Android and iPhone","timezone":"Europe/Berlin","twinType":"performance","parentId":"343a6a61f5ef48c899b13f9c1be45b07","typeId":"iiotuxpc.mobilephone","location":null,"fileAssignments":[],"variables":[],"aspects":[{"name":"connectivityStatus","variables":[{"name":"connected","value":"false"},{"name":"lastUpdated","value":"2023-02-22T20:04:49Z"}]}],"locks":[{"service":"AgentManagement","reason":"Agent is onboarded, agent cannot be deleted. Only offboarded agents can be deleted.","reasonCode":"agentmanagement.agent.onboarded","_links":{"self":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/574fbc1ab7964fa3a6acf1173707a256/locks/c97267a7ea3d43ecbd961ad240a2db50"}},"id":"c97267a7ea3d43ecbd961ad240a2db50"}],"deleted":null,"sharing":{"modes":[]},"_links":{"self":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/574fbc1ab7964fa3a6acf1173707a256"},"aspects":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/574fbc1ab7964fa3a6acf1173707a256/aspects"},"variables":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/574fbc1ab7964fa3a6acf1173707a256/variables"},"location":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/574fbc1ab7964fa3a6acf1173707a256/location"},"parent":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/343a6a61f5ef48c899b13f9c1be45b07"}}},{"assetId":"9c722dc9893e44e4a522295ebf2879b5","tenantId":"iiotuxpc","name":"RPI Device","etag":0,"externalId":null,"t2Tenant":null,"subTenant":null,"description":"Digital representation of a Raspberry Pi. A Raspberry Pi is a credit-card sized computer","timezone":"Europe/Berlin","twinType":"performance","parentId":"343a6a61f5ef48c899b13f9c1be45b07","typeId":"core.starteragentrpiassettype","location":null,"fileAssignments":[],"variables":[],"aspects":[{"name":"connectivityStatus","variables":[{"name":"connected","value":"false"}]}],"locks":[],"deleted":null,"sharing":{"modes":[]},"_links":{"self":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/9c722dc9893e44e4a522295ebf2879b5"},"aspects":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/9c722dc9893e44e4a522295ebf2879b5/aspects"},"variables":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/9c722dc9893e44e4a522295ebf2879b5/variables"},"location":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/9c722dc9893e44e4a522295ebf2879b5/location"},"parent":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/343a6a61f5ef48c899b13f9c1be45b07"}}}]},"_links":{"self":{"href":"https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets?basicFieldsOnly=false&page=0&size=10&sort=name,id,asc"}},"page":{"size":10,"totalElements":4,"totalPages":1,"number":0}}
```

## time series
### get timeseries data
- time should be in ISO8601 format: YYYY-MM-DDTHH:MM:SS.SSSZ (2023-02-21T02:01:01.001Z)

- end_point = `"iottimeseries/v3/timeseries/iottimeseries/v3/timeseries/574fbc1ab7964fa3a6acf1173707a256/connectivityStatus?from=2023-02-01T02:01:01.001Z&to=2023-02-01T02:03:01.001Z"`

- probable template:
```https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/<asset_id>/<aspect>/?from=<start_time>&to=<end_time>&select=<variables>&interval=<interval>&sort=<sort_order>&limit=<max_num_results>'```

```python
# get list of aspects a asset
asset_name = "machine"
asset_Id = "60bf86d1d051416f853b1e22f3714b8c"
aspect_name = "real_log"
from_condition = "2023-02-20T02:00:01.001Z"
to_condition = "2023-02-20T02:02:01.001Z"
data_condition = "?from=" + from_condition + "&to=" + to_condition
end_point = "iottimeseries/v3/timeseries/" + asset_Id + "/" + aspect_name + data_condition

base_url = "https://gateway.eu1.mindsphere.io/api/"
url = base_url + end_point

payload={}
headers = {
  'Authorization': 'Bearer ' + bearer_token
}

time_series_response = requests.request("GET", url, headers=headers, data=payload)
print(time_series_response.text)
time_series=json.loads(time_series_response.text)
# print(time_series)

```

### put time series data

- time should be in ISO8601 format: YYYY-MM-DDTHH:MM:SS.SSSZ (2023-02-21T02:01:01.001Z)
- all the write json dictionary should have _time as a compulsary MindSphere internal variable for time series database.
- printing `response.text` is important to know the feedback of PUT process where we can know if any error occured.
```python
payload = json.dumps([
    {
    "_time":"2023-02-20T02:01:01.001Z",
    "activity_type":"started",
    "machine_id":"machine_1",
    "part_id":"100",
    "queue":"queue 1",
    "timestamp":"2023-02-20T02:01:01.001Z"
    },
    {
    "_time":"2023-02-20T02:02:01.001Z",
    "activity_type":"finished",
    "machine_id":"machine_1",
    "part_id":"100",
    "queue":"queue 1",
    "timestamp":"2023-02-20T02:02:01.001Z"
    }
])

#--- process the API PUT sequence
asset_Id = "60bf86d1d051416f853b1e22f3714b8c"
aspect_name = "real_log"
end_point = "iottimeseries/v3/timeseries/" + asset_Id + "/" + aspect_name
base_url = "https://gateway.eu1.mindsphere.io/api/"

url = base_url + end_point
data_json = json.dumps(data)
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': "Bearer " + bearer_token
}

response = requests.request("PUT", url, headers=headers, data=payload)
if not response.text:
  print("Data PUT successfully.")
else:print("Error:\n\t",response.text)

```

example:
```json
[
    {
        "x": 0.22505496442317963,
        "y": 5.614402770996094,
        "z": 7.467514991760254,
        "_time": "2023-02-22T19:56:44.521Z"
    },
    {
        "x": 0.2059013396501541,
        "y": 5.748478412628174,
        "z": 7.979874134063721,
        "_time": "2023-02-22T19:56:44.620Z"
    },
    {
        "x": 0.5482721924781799,
        "y": 5.5114521980285645,
        "z": 8.149862289428711,
        "_time": "2023-02-22T19:56:44.819Z"
    },
    {
        "x": 0.4884171485900879,
        "y": 5.509057998657227,
        "z": 8.042123794555664,
        "_time": "2023-02-22T19:56:44.920Z"
    }]
    ```
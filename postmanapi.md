## access token
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
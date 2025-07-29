from dependencies import *

def revoke_access_token(APP_KEY, APP_SECRET, TOKEN, URL_BASE):
    headers = {"content-type":"application/json"}
    body = {"grant_type":"client_credentials",
    "appkey":APP_KEY, 
    "appsecret":APP_SECRET,
    "token":TOKEN}
    PATH = "oauth2/revokeP"
    URL = f"{URL_BASE}/{PATH}"

    res = requests.post(URL, headers=headers, data=json.dumps(body))
    message = res.json()["message"]
    return message
from dependencies import *

def get_access_token(APP_KEY, APP_SECRET, URL_BASE):
    """토큰 발급"""
    headers = {"content-type":"application/json"}
    body = {"grant_type":"client_credentials",
    "appkey":APP_KEY, 
    "appsecret":APP_SECRET}
    PATH = "oauth2/tokenP"
    URL = f"{URL_BASE}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    ACCESS_TOKEN = res.json()["access_token"]
    ACCESS_TOKEN_EXPIRE = res.json()["access_token_token_expired"]

    print("token 발행! 만료 시간", ACCESS_TOKEN_EXPIRE)
    return ACCESS_TOKEN, ACCESS_TOKEN_EXPIRE
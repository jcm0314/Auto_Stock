from dependencies import *

def get_balance(ACCESS_TOKEN):
    """현금 잔고조회"""
    PATH = "uapi/domestic-stock/v1/trading/inquire-psbl-order"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"VTTC8434R", #실전투자:TTTC8434R ,   #모의투자:VTTC8434R
        "custtype":"P",
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "AFHR_FLPR_YN":"N",
        "OFL_YN":"",
        "INQR_DVSN":"00",
        "UNPR_DVSN":"01",
        "FUND_STTL_ICLD_YN":"N",
        "FNCG_AMT_AUTO_RDPT_YN":"N",
        "PRCS_DVSN":"01",
        "COST_ICLD_YN":"N",
        "CTX_AREA_FK100":"",
        "CTX_AREA_NK100":""
    }
    res = requests.get(URL, headers=headers, params=params)
    print(res.json())
    cash = res.json()['output2'][0]['dnca_tot_amt']

    return int(cash)
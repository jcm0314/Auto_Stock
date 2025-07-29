from dependencies import *
from send_message import *

def get_stock_balance(ACCESS_TOKEN):
    """주식 잔고조회"""
    PATH = "/uapi/domestic-stock/v1/trading/inquire-balance"
    URL = f"{URL_BASE}/{PATH}"

    headers = {
        "content-type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appkey":APP_KEY,
        "appsecret":APP_SECRET,
        "tr_id":"VTTC8434R",    #실전투자:TTTC8434R ,   #모의투자:VTTC8434R
        "custtype":"P",
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",     
        "INQR_DVSN": "02",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "01",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": ""
    }

    res = requests.get(URL, headers=headers, params=params)
    print(res.json())
    stock_list = res.json()['output1']      # 주식 금액
    evaluation = res.json()['output2']      # 평가 금액
    stock_dict = {}

    send_message(f"====주식 보유잔고====")
    for stock in stock_list:
        if int(stock['hldg_qty']) > 0:
            stock_dict[stock['pdno']] = stock['hldg_qty']
            send_message(f"{stock['prdt_name']}({stock['pdno']}): {stock['hldg_qty']}주")
            time.sleep(0.1)

    if len(stock_list) == 0:
        send_message(f"====주식 미보유====")
    else:  
        send_message(f"주식 평가 금액: {evaluation[0]['scts_evlu_amt']}원")
        time.sleep(0.1)
        send_message(f"평가 손익 합계: {evaluation[0]['evlu_pfls_smtl_amt']}원")
        time.sleep(0.1)
    
    send_message(f"총 평가 금액: {evaluation[0]['tot_evlu_amt']}원")
    time.sleep(0.1)
    return stock_dict
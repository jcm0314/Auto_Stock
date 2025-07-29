from dependencies import *
from send_message import *
from hashkey import *
from get_access_token import *
import pandas as pd
import os

def test(code, ACCESS_TOKEN):
    yesterday = datetime.now() - timedelta(1)
    other_day = yesterday - timedelta(100)

    yesterday = yesterday.strftime('%Y%m%d')
    other_day = other_day.strftime('%Y%m%d')

    PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{URL_BASE}/{PATH}"
    data = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": code,
        "FID_INPUT_DATE_1": other_day,
        "FID_INPUT_DATE_2": yesterday,
        "fid_org_adj_prc": "0",
        "fid_period_div_code": "D"
    }
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"FHKST03010100",        #TTTC0801U 실전 투자   VTTC0801U  모의 투자
        "custtype":"P",
    }
    res = requests.get(URL, headers=headers, params=data)
    
    if res.status_code == 200:
        data = res.json()['output2']

        # Pandas DataFrame으로 변환
        df = pd.DataFrame(data)
        
        df['date'] = pd.to_datetime(df['stck_bsop_date'])
        df = df.set_index('date')

        columns = ['5', '9', '10', '12', '14', '20', '26', '30', '60']

        # 이동평균 계산
        for i in columns:
            df[f'MA{i}'] = df['stck_clpr'].rolling(window=int(i)).mean()

        # average_df에 이동평균 값 저장
        data_list = [df[f'MA{i}'].fillna(method='bfill').iloc[0] for i in columns]
        average_df = pd.DataFrame([data_list], columns=columns, index=[code])
        print(average_df)
        
        # CSV 파일 저장
        csv_file = f"data/report.csv"
        if os.path.exists(csv_file):
            average_df.to_csv(csv_file, mode='a', index=True, header=False)
        else:
            average_df.to_csv(csv_file, mode='w', index=True)

def dump_yaml():
    ACCESS_TOKEN, ACCESS_TOKEN_EXPIRE = get_access_token(APP_KEY, APP_SECRET, URL_BASE)
    data_to_write = {
        'TOKEN': ACCESS_TOKEN,
        'EXPIRE': ACCESS_TOKEN_EXPIRE
    }

    # 파일에 새로 작성
    with open('settings/token.yaml','w', encoding='UTF-8') as f:
        yaml.dump(data_to_write, f, allow_unicode=True, default_flow_style=False)

    return ACCESS_TOKEN

# Token 발행
ACCESS_TOKEN = ""
# 파일을 읽기/쓰기 모드로 열기
with open('settings/token.yaml','r+', encoding='UTF-8') as f:
    _get_token = yaml.load(f, Loader=yaml.FullLoader)
    try:        # token이 있는 지 확인.  확인 했다면 만료시간 확인하기.
        ACCESS_TOKEN = _get_token['TOKEN']
        expiry_str = _get_token['EXPIRE']

        expiry_time = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()

        if current_time > expiry_time:  # 만료 시간이 지나서 새로운 토큰 발행
            ACCESS_TOKEN = dump_yaml()

    except: # 새로운 토큰 발행
        ACCESS_TOKEN = dump_yaml()

symbol_list = ["005930","035720","000660","069500"]

def check_csv_file():

    # CSV 파일 불러오기
    df = pd.read_csv('data/report.csv', dtype={0:'string'}, index_col=0)
    print(df)
    print("----------------------------------------------")
    print(df.loc["005930"])


for code in symbol_list:
    time.sleep(2)
    test(code, ACCESS_TOKEN)


check_csv_file()
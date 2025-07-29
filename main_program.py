from dependencies import *
from send_message import *
from revoke_access_token import *
from get_access_token import *
from get_balance import *
from get_stock_balance import *
from buy_stock import *
from sell_stock import *
from get_target_price import *
from get_current_price import *

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

def check_trading_hours():
    # 현재 날짜와 시간 가져오기
    t_now = datetime.now()
    
    # 주식 거래 시작 및 종료 시간 설정
    t_start = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
    t_end = t_now.replace(hour=15, minute=30, second=0, microsecond=0)
    
    # 오늘의 요일 확인 (월요일: 0, 화요일: 1, ... , 토요일: 5, 일요일: 6)
    today = t_now.weekday()
    
    # 주말 확인 (토요일: 5, 일요일: 6)
    if today == 5 or today == 6:
        send_message("주말이므로 거래를 종료합니다.")
        return False
    
    # 거래 시간 확인
    if t_now < t_start or t_now > t_end:
        send_message("====지금은 주식 거래 시간이 아닙니다.====")
        send_message("====거래를 종료합니다.====")
        return False
    
    # 거래 시간 내라면 True 반환
    return True


try:
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
        
    send_message("====현재 운용 자산====")

    #message = revoke_access_token(APP_KEY, APP_SECRET, TOKEN, URL_BASE)        # 토큰 revoke
    total_cash = get_balance(ACCESS_TOKEN) # 보유 현금 조회
    send_message(f"주문 가능 현금 잔고: {total_cash}원")

    stock_dict = get_stock_balance(ACCESS_TOKEN) # 보유 주식 조회

    # ================================================================ 

    symbol_list = ["005930","035720","000660","069500"] # 매수 희망 종목 리스트
    bought_list = [] # 매수 완료된 종목 리스트

    for sym in stock_dict.keys():
        bought_list.append(sym)

    target_buy_count = 3 # 매수할 종목 수
    buy_percent = 0.33 # 종목당 매수 금액 비율
    buy_amount = total_cash * buy_percent  # 종목별 주문 금액 계산
    soldout = False

    t_now = datetime.now()
    t_9 = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
    t_start = t_now.replace(hour=9, minute=0, second=5, microsecond=0)
    t_sell = t_now.replace(hour=15, minute=15, second=0, microsecond=0)
    t_exit = t_now.replace(hour=15, minute=29, second=30,microsecond=0)

    send_message("")
    send_message("====주식 자동매매 프로그램을 시작합니다.====")
    send_message("")
    send_message("====주식 거래를 시작합니다.====")
    while True:
        # 주식 거래 시간 확인
        if check_trading_hours():
            pass
        else:
            break
        if t_9 < t_now < t_start and soldout == False: # 잔여 수량 매도
            for sym, qty in stock_dict.items():
                sell(sym, qty, ACCESS_TOKEN)
            soldout == True
            bought_list = []
            stock_dict = get_stock_balance(ACCESS_TOKEN)
        if t_start < t_now < t_sell :  # AM 09:05 ~ PM 03:15 : 매수
            for sym in symbol_list:
                if len(bought_list) < target_buy_count:
                    if sym in bought_list:
                        continue
                    target_price = get_target_price(sym, ACCESS_TOKEN)
                    current_price = get_current_price(sym, ACCESS_TOKEN)
                    if target_price < current_price:
                        buy_qty = 0  # 매수할 수량 초기화
                        buy_qty = int(buy_amount // current_price)
                        if buy_qty > 0:
                            send_message(f"{sym} 목표가 달성({target_price} < {current_price}) 매수를 시도합니다.")
                            result = buy(sym, buy_qty, ACCESS_TOKEN)
                            if result:
                                soldout = False
                                bought_list.append(sym)
                                get_stock_balance(ACCESS_TOKEN)
                    time.sleep(1)
            time.sleep(1)
            if t_now.minute == 30 and t_now.second <= 5: 
                get_stock_balance(ACCESS_TOKEN)
                time.sleep(5)
        if t_sell < t_now < t_exit:  # PM 03:15 ~ PM 03:20 : 일괄 매도
            if soldout == False:
                stock_dict = get_stock_balance(ACCESS_TOKEN)
                for sym, qty in stock_dict.items():
                    sell(sym, qty, ACCESS_TOKEN)
                soldout = True
                bought_list = []
                time.sleep(1)
        if t_exit < t_now:  # PM 03:20 ~ :프로그램 종료
            send_message("====프로그램을 종료합니다.====")
            break
    
    send_message("")
    send_message("====주식 자동매매 프로그램을 종료합니다====")
    send_message("")
except Exception as e:
    send_message(f"[오류 발생]{e}")
    time.sleep(1)
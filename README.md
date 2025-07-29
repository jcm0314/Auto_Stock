# Auto_Stock 📈

김덕륜과 함께하는 주식자동화 프로젝트(2024.12.14 ~ )

## 📋 프로젝트 개요

이 프로젝트는 한국투자증권 API를 활용한 자동 주식 거래 시스템입니다. 지정된 종목들을 자동으로 매수/매도하여 수익을 극대화하는 것을 목표로 합니다.

## 🚀 주요 기능

- **자동 매수/매도**: 설정된 조건에 따라 자동으로 주식 거래
- **실시간 모니터링**: Discord를 통한 실시간 거래 알림
- **거래 시간 관리**: 주식 거래 시간(9:00-15:30)에만 거래 실행
- **토큰 자동 관리**: API 토큰 자동 갱신 및 관리
- **포트폴리오 분산**: 여러 종목에 자산 분산 투자

## 📁 프로젝트 구조

```
Auto_Stock/
├── main_program.py          # 메인 프로그램
├── dependencies.py          # 의존성 및 설정 로드
├── buy_stock.py            # 주식 매수 기능
├── sell_stock.py           # 주식 매도 기능
├── get_balance.py          # 계좌 잔고 조회
├── get_stock_balance.py    # 보유 주식 조회
├── get_current_price.py    # 현재가 조회
├── get_target_price.py     # 목표가 계산
├── get_access_token.py     # API 토큰 발급
├── revoke_access_token.py  # API 토큰 해지
├── send_message.py         # Discord 메시지 전송
├── discord_bot.py          # Discord 봇 기능
├── hashkey.py              # API 인증 해시키 생성
├── stock_program.bat       # Windows 실행 배치 파일
├── test.py                 # 테스트 코드
├── settings/               # 설정 파일들
│   ├── fake_config.yaml    # 개발용 설정
│   ├── real_config.yaml    # 운영용 설정
│   ├── token.yaml          # API 토큰 저장
│   └── main.py             # 설정 관리
├── data/                   # 데이터 파일
│   └── report.csv          # 거래 리포트
└── testing/                # 테스트 관련 파일들
```

## 🛠️ 설치 및 설정

### 1. 필수 요구사항

- Python 3.7 이상
- 한국투자증권 계좌
- Discord 웹훅 URL

### 2. 의존성 설치

```bash
pip install requests
pip install pyyaml
```

### 3. 설정 파일 구성

`settings/fake_config.yaml` 또는 `settings/real_config.yaml` 파일을 다음과 같이 설정:

```yaml
APP_KEY: "your_app_key"
APP_SECRET: "your_app_secret"
CANO: "your_account_number"
ACNT_PRDT_CD: "01"
DISCORD_WEBHOOK_URL: "your_discord_webhook_url"
URL_BASE: "https://openapi.koreainvestment.com:9443"
```

### 4. 실행 방법

**Windows:**
```bash
stock_program.bat
```

**Python 직접 실행:**
```bash
python main_program.py
```

## ⚙️ 설정 옵션

### 거래 설정
- `symbol_list`: 매수 희망 종목 리스트 (종목코드)
- `target_buy_count`: 매수할 종목 수
- `buy_percent`: 종목당 매수 금액 비율 (0.33 = 33%)

### 거래 시간
- **매수 시작**: 09:00:05
- **매도 시작**: 15:15:00
- **거래 종료**: 15:29:30

## 📊 현재 지원 종목

기본 설정된 종목:
- `005930`: 삼성전자
- `035720`: 카카오
- `000660`: SK하이닉스
- `069500`: KODEX 200

## 🔔 알림 기능

Discord를 통해 다음 정보들을 실시간으로 받을 수 있습니다:
- 거래 시작/종료 알림
- 매수/매도 실행 알림
- 계좌 잔고 정보
- 보유 주식 현황
- 에러 및 예외 상황

## ⚠️ 주의사항

1. **실제 거래**: 이 프로그램은 실제 돈으로 거래하므로 신중하게 사용하세요.
2. **API 제한**: 한국투자증권 API 사용량 제한을 확인하세요.
3. **시장 위험**: 주식 투자는 원금 손실 위험이 있습니다.
4. **테스트**: 실제 거래 전에 충분한 테스트를 진행하세요.

## 🐛 문제 해결

### 일반적인 문제들

1. **토큰 만료**: 프로그램이 자동으로 토큰을 갱신합니다.
2. **거래 시간 외**: 거래 시간(9:00-15:30)에만 거래가 실행됩니다.
3. **잔고 부족**: 충분한 현금이 있는지 확인하세요.

## 📈 성능 모니터링

거래 결과는 `data/report.csv` 파일에 자동으로 저장됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 연락처

프로젝트 관련 문의사항이 있으시면 이슈를 생성해 주세요.

---

**⚠️ 투자 경고**: 이 프로그램은 교육 및 연구 목적으로 제작되었습니다. 실제 투자에 사용하기 전에 충분한 검토와 테스트를 진행하시기 바랍니다.

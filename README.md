# 괌 날씨 데이터 분석 프로젝트 🌴

## 📋 프로젝트 개요
괌의 날씨 데이터를 분석하여 기후 패턴을 이해하고 기후 변화에 대한 통찰력을 얻기 위한 프로젝트입니다.

### 🎯 주요 목표
- 괌의 2020-2022년 날씨 패턴 분석
- National Weather Service API를 활용한 실시간 예보 데이터 수집
- 과거 데이터와 현재 예보의 비교 분석
- 시각화를 통한 인사이트 도출

## 🗂️ 프로젝트 구조

```
guam-weather-analysis/
├── data/                          # 원본 CSV 데이터 (2020-2022)
│   ├── 2020_01.csv ~ 2020_12.csv
│   ├── 2021_01.csv ~ 2021_12.csv
│   └── 2022_01.csv ~ 2022_12.csv
├── src/                           # Python 모듈
│   ├── data_processing.py         # 데이터 전처리 함수
│   ├── visualization.py           # 시각화 함수
│   └── api_client.py              # API 클라이언트
├── notebooks/                     # Jupyter 노트북
│   ├── 01_csv_analysis.ipynb      # CSV 데이터 분석
│   └── 02_api_analysis.ipynb      # API 데이터 분석
├── results/                       # 분석 결과 및 그래프
├── requirements.txt               # 필요한 패키지 목록
└── README.md                      # 프로젝트 설명서
```

## 🚀 시작하기

### 1. 환경 설정
```bash
# 필요한 패키지 설치
pip install -r requirements.txt

# Jupyter 노트북 실행
jupyter notebook
```

### 2. 분석 실행 순서
1. **CSV 데이터 분석**: `notebooks/01_csv_analysis.ipynb` 실행
2. **API 데이터 분석**: `notebooks/02_api_analysis.ipynb` 실행

## 📊 주요 기능

### 1. CSV 데이터 분석 (`01_csv_analysis.ipynb`)
- 2020-2022년 괌 날씨 CSV 데이터 통합 및 전처리
- 화씨 → 섭씨, 인치 → mm 단위 변환
- 연도별/월별 통계 분석
- 다양한 시각화 그래프 생성

### 2. API 데이터 분석 (`02_api_analysis.ipynb`)
- National Weather Service API 연동
- 7일 날씨 예보 데이터 수집
- 실시간 예보와 과거 데이터 비교
- 예보 정확도 및 패턴 분석

### 3. 데이터 처리 모듈 (`src/`)
- **data_processing.py**: 단위 변환, 데이터 정제, 통계 계산
- **visualization.py**: 그래프 생성, 대시보드 제작
- **api_client.py**: API 호출, 데이터 파싱, 오류 처리

## 📈 주요 분석 결과

### 🌡️ 기온 특성
- 연중 매우 안정적인 기온 유지 (열대 해양성 기후)
- 계절간 기온 차이 매우 작음 (약 2-3°C)
- 평균 기온: 27-28°C 범위

### 🌧️ 강수량 패턴
- 연간 강수량: 약 2,000-3,000mm
- 6-9월 우기, 12-3월 건기 패턴
- 연도별 변동성 존재하나 안정적인 편

### 📊 기후 변화 신호
- 여름철 평년 대비 기온 상승 경향
- 극단적 계절성 심화 가능성
- 장기 모니터링 필요

## 🛠️ 기술 스택
- **Python 3.8+**
- **pandas**: 데이터 처리 및 분석
- **matplotlib, seaborn**: 데이터 시각화
- **requests**: API 통신
- **jupyter**: 노트북 환경

## 📋 데이터 소스
- **CSV 데이터**: National Weather Service (NWS)
- **API 데이터**: https://api.weather.gov
- **데이터 기간**: 2020년 1월 - 2022년 12월

## 🔧 주요 함수

### 데이터 처리
```python
# 단위 변환
fahrenheit_to_celsius(fahrenheit)  # 화씨 → 섭씨
inches_to_mm(inches)               # 인치 → mm

# 데이터 로딩 및 전처리
load_all_csv_files(data_dir)       # CSV 파일 통합
preprocess_weather_data(df)        # 데이터 전처리
```

### 시각화
```python
# 그래프 생성
plot_monthly_temperature_by_year(df)    # 연도별 월기온
plot_monthly_precipitation_by_year(df)  # 연도별 월강수량
plot_temperature_departure(df)          # 기온 편차
create_comprehensive_dashboard(df)      # 종합 대시보드
```

### API 클라이언트
```python
# 날씨 예보 조회
get_guam_forecast()                     # 괌 7일 예보
compare_with_historical(forecast, hist) # 과거 데이터 비교
```

## 📁 결과 파일
분석 완료 후 `results/` 디렉토리에 다음 파일들이 생성됩니다:
- `processed_weather_data.csv`: 전처리된 날씨 데이터
- `monthly_temperature_by_year.png`: 연도별 월기온 그래프
- `monthly_precipitation_by_year.png`: 연도별 월강수량 그래프
- `yearly_summary.png`: 연간 요약 그래프
- `temperature_departure.png`: 기온 편차 그래프
- `comprehensive_dashboard.png`: 종합 대시보드
- `forecast_data.csv`: 예보 데이터 (API 성공시)
- `forecast_visualization.png`: 예보 시각화 (API 성공시)

## ⚠️ 주의사항
1. **API 제한**: National Weather Service API는 괌 지역 데이터 제공에 제한이 있을 수 있습니다.
2. **네트워크 연결**: API 호출시 인터넷 연결이 필요합니다.
3. **한글 폰트**: macOS 환경에서 AppleGothic 폰트를 사용합니다.

## 🔄 향후 개선 계획
- 더 많은 연도 데이터 추가 분석
- 다른 날씨 API 서비스 연동
- 머신러닝을 활용한 예측 모델 개발
- 인터랙티브 웹 대시보드 구축

## 👥 기여하기
1. 이 저장소를 포크합니다
2. 새로운 기능 브랜치를 만듭니다
3. 변경사항을 커밋합니다
4. 브랜치에 푸시합니다
5. Pull Request를 생성합니다

## 📞 문의사항
프로젝트에 대한 문의나 제안사항이 있으시면 Issue를 통해 연락해주세요.

---
*괌의 아름다운 날씨를 데이터로 탐험해보세요! 🏝️* 
"""
National Weather Service API를 활용한 날씨 데이터 수집 모듈
"""
import requests
import pandas as pd
from datetime import datetime

class WeatherAPI:
    """National Weather Service API 클라이언트"""
    
    def __init__(self):
        self.base_url = "https://api.weather.gov"
        self.session = requests.Session()
        # API 요청시 User-Agent 헤더 추가 (API 요구사항)
        self.session.headers.update({
            'User-Agent': 'GuamWeatherAnalysis/1.0 (educational-project)'
        })
    
    def get_location_info(self, latitude, longitude):
        """위도/경도를 기반으로 위치 정보 조회"""
        try:
            points_url = f"{self.base_url}/points/{latitude},{longitude}"
            response = self.session.get(points_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"위치 정보 조회 실패: {e}")
            return None
    
    def get_forecast_data(self, latitude, longitude):
        """7일 날씨 예보 데이터 조회"""
        try:
            # 1. 위치 정보 조회
            location_data = self.get_location_info(latitude, longitude)
            if not location_data:
                return None
            
            # 2. 예보 URL 추출
            forecast_url = location_data['properties']['forecast']
            
            # 3. 예보 데이터 조회
            forecast_response = self.session.get(forecast_url)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            return forecast_data
            
        except requests.RequestException as e:
            print(f"예보 데이터 조회 실패: {e}")
            return None
        except KeyError as e:
            print(f"응답 데이터 구조 오류: {e}")
            return None
    
    def process_forecast_data(self, forecast_data):
        """예보 데이터를 DataFrame으로 변환"""
        if not forecast_data:
            return None
        
        try:
            periods = forecast_data['properties']['periods']
            
            # 낮과 밤 데이터 분리
            day_periods = [p for p in periods if p['isDaytime']]
            night_periods = [p for p in periods if not p['isDaytime']]
            
            # 날짜별 최고/최저 기온 데이터 생성
            dates = []
            highs_f = []
            lows_f = []
            
            # 데이터 길이 맞추기
            min_length = min(len(day_periods), len(night_periods))
            
            for i in range(min_length):
                date_str = day_periods[i]['startTime'][:10]
                dates.append(date_str)
                highs_f.append(day_periods[i]['temperature'])
                lows_f.append(night_periods[i]['temperature'])
            
            # 화씨를 섭씨로 변환
            highs_c = [(temp - 32) * 5/9 for temp in highs_f]
            lows_c = [(temp - 32) * 5/9 for temp in lows_f]
            
            # DataFrame 생성
            df = pd.DataFrame({
                'Date': dates,
                'High (°C)': highs_c,
                'Low (°C)': lows_c,
                'High (°F)': highs_f,
                'Low (°F)': lows_f
            })
            
            # Date 컬럼을 datetime으로 변환
            df['Date'] = pd.to_datetime(df['Date'])
            
            return df
            
        except Exception as e:
            print(f"데이터 처리 중 오류 발생: {e}")
            return None

def get_guam_forecast():
    """괌의 7일 날씨 예보 조회"""
    # 괌의 좌표
    GUAM_LAT = 13.4443
    GUAM_LON = 144.7937
    
    api_client = WeatherAPI()
    
    print("괌 날씨 예보 데이터를 조회 중...")
    forecast_data = api_client.get_forecast_data(GUAM_LAT, GUAM_LON)
    
    if forecast_data:
        print("예보 데이터 조회 성공!")
        df = api_client.process_forecast_data(forecast_data)
        return df
    else:
        print("예보 데이터 조회 실패")
        return None

def compare_with_historical(forecast_df, historical_df):
    """예보 데이터와 과거 데이터 비교"""
    if forecast_df is None or historical_df is None:
        return None
    
    try:
        # 현재 날짜 기준으로 과거 같은 시기 데이터 추출
        current_month = datetime.now().month
        historical_same_month = historical_df[historical_df['Month'] == current_month]
        
        # 과거 같은 달의 평균 기온 계산
        hist_avg_max = historical_same_month['Maximum'].mean()
        hist_avg_min = historical_same_month['Minimum'].mean()
        
        # 예보 데이터의 평균 계산
        forecast_avg_max = forecast_df['High (°C)'].mean()
        forecast_avg_min = forecast_df['Low (°C)'].mean()
        
        comparison = {
            '과거 평균 최고기온': hist_avg_max,
            '과거 평균 최저기온': hist_avg_min,
            '예보 평균 최고기온': forecast_avg_max,
            '예보 평균 최저기온': forecast_avg_min,
            '최고기온 차이': forecast_avg_max - hist_avg_max,
            '최저기온 차이': forecast_avg_min - hist_avg_min
        }
        
        return comparison
        
    except Exception as e:
        print(f"비교 분석 중 오류 발생: {e}")
        return None 
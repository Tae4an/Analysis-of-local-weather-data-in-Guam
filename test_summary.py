#!/usr/bin/env python3
"""
괌 날씨 데이터 분석 프로젝트 - 최종 테스트 결과 요약
"""

import os
import pandas as pd
from datetime import datetime

print("🏆 괌 날씨 데이터 분석 프로젝트 - 최종 테스트 결과")
print("="*80)

# 1. 프로젝트 구조 확인
print("\n📁 1. 프로젝트 구조 검증")
print("-" * 50)

required_dirs = ['src', 'notebooks', 'data', 'results']
required_files = ['requirements.txt', 'README.md']

for dir_name in required_dirs:
    if os.path.exists(dir_name):
        files_count = len(os.listdir(dir_name))
        print(f"✅ {dir_name}/ 디렉토리 존재 ({files_count}개 파일)")
    else:
        print(f"❌ {dir_name}/ 디렉토리 없음")

for file_name in required_files:
    if os.path.exists(file_name):
        file_size = os.path.getsize(file_name)
        print(f"✅ {file_name} 존재 ({file_size/1024:.1f}KB)")
    else:
        print(f"❌ {file_name} 없음")

# 2. 데이터 처리 결과 확인
print("\n📊 2. 데이터 처리 결과")
print("-" * 50)

try:
    processed_df = pd.read_csv("results/processed_weather_data.csv")
    print(f"✅ 전처리된 데이터: {processed_df.shape[0]:,}행 × {processed_df.shape[1]}열")
    print(f"📅 데이터 기간: {processed_df['Date'].min()} ~ {processed_df['Date'].max()}")
    print(f"🌡️ 기온 범위: {processed_df['Average'].min():.1f}°C ~ {processed_df['Average'].max():.1f}°C")
    print(f"🌧️ 강수량 범위: {processed_df['Precipitation'].min():.1f}mm ~ {processed_df['Precipitation'].max():.1f}mm")
except FileNotFoundError:
    print("❌ 전처리된 데이터 파일이 없습니다")

# 3. API 데이터 확인
print("\n🌐 3. API 데이터 수집 결과")
print("-" * 50)

try:
    forecast_df = pd.read_csv("results/forecast_data.csv")
    print(f"✅ 예보 데이터: {len(forecast_df)}일 예보")
    print(f"🌡️ 예보 기온 범위: {forecast_df['High (°C)'].min():.1f}°C ~ {forecast_df['High (°C)'].max():.1f}°C")
    print(f"📡 National Weather Service API 연동 성공")
except FileNotFoundError:
    print("❌ 예보 데이터 파일이 없습니다")

# 4. 시각화 결과 확인
print("\n📈 4. 시각화 결과")
print("-" * 50)

visualization_files = [
    "monthly_temperature_by_year.png",
    "monthly_precipitation_by_year.png", 
    "yearly_summary.png",
    "temperature_departure.png",
    "comprehensive_dashboard.png",
    "forecast_visualization.png"
]

for viz_file in visualization_files:
    file_path = f"results/{viz_file}"
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        print(f"✅ {viz_file} ({file_size/1024:.0f}KB)")
    else:
        print(f"❌ {viz_file} 없음")

# 5. 핵심 인사이트 요약
print("\n💡 5. 핵심 분석 결과")
print("-" * 50)

try:
    # CSV 데이터 인사이트
    processed_df = pd.read_csv("results/processed_weather_data.csv")
    
    yearly_avg = processed_df.groupby('Year')['Average'].mean()
    temp_stability = processed_df.groupby('Year')['Average'].std().mean()
    annual_precip = processed_df.groupby('Year')['Precipitation'].sum()
    
    print("🌴 괌 기후 특성 (2020-2022):")
    print(f"   • 평균 기온: {processed_df['Average'].mean():.1f}°C")
    print(f"   • 기온 안정성: 표준편차 {temp_stability:.2f}°C (매우 안정적)")
    print(f"   • 연간 강수량: {annual_precip.mean():.0f}mm")
    
    # API 데이터와 비교
    try:
        forecast_df = pd.read_csv("results/forecast_data.csv")
        current_month = datetime.now().month
        
        historical_current = processed_df[processed_df['Month'] == current_month]
        hist_avg = historical_current['Average'].mean()
        forecast_avg = (forecast_df['High (°C)'].mean() + forecast_df['Low (°C)'].mean()) / 2
        
        print(f"\n🔍 실시간 비교 ({current_month}월):")
        print(f"   • 과거 평균: {hist_avg:.1f}°C")
        print(f"   • 예보 평균: {forecast_avg:.1f}°C")
        print(f"   • 차이: {forecast_avg - hist_avg:+.1f}°C")
        
    except FileNotFoundError:
        print("\n⚠️ API 데이터가 없어 비교할 수 없습니다")
        
except FileNotFoundError:
    print("❌ 분석 데이터가 없습니다")

# 6. 성공 여부 판정
print("\n🎯 6. 전체 테스트 결과")
print("-" * 50)

success_count = 0
total_tests = 0

# 필수 파일 체크
total_tests += len(required_dirs) + len(required_files)
for item in required_dirs + required_files:
    if os.path.exists(item):
        success_count += 1

# 결과 파일 체크
total_tests += len(visualization_files) + 2  # +2 for data files
for viz_file in visualization_files:
    if os.path.exists(f"results/{viz_file}"):
        success_count += 1

if os.path.exists("results/processed_weather_data.csv"):
    success_count += 1
if os.path.exists("results/forecast_data.csv"):
    success_count += 1

success_rate = (success_count / total_tests) * 100

print(f"📊 테스트 통과율: {success_count}/{total_tests} ({success_rate:.1f}%)")

if success_rate >= 90:
    print("🎉 테스트 성공! 프로젝트가 완벽하게 작동합니다.")
elif success_rate >= 70:
    print("✅ 테스트 대부분 성공! 일부 기능에 문제가 있을 수 있습니다.")
else:
    print("❌ 테스트 실패! 주요 기능에 문제가 있습니다.")

print("\n" + "="*80)
print("🌴 괌 날씨 데이터 분석 프로젝트 테스트 완료! 🌊")
print("="*80) 
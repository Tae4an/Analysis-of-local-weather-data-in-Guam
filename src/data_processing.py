"""
괌 날씨 데이터 전처리 유틸리티 모듈
"""
import pandas as pd
import os
import numpy as np

def fahrenheit_to_celsius(fahrenheit):
    """화씨를 섭씨로 변환"""
    return (fahrenheit - 32) * 5.0/9.0

def inches_to_mm(inches):
    """인치를 밀리미터로 변환"""
    return inches * 25.4

def load_all_csv_files(data_dir="data"):
    """data 디렉토리의 모든 CSV 파일을 읽어서 하나의 DataFrame으로 결합"""
    csv_files = sorted([f for f in os.listdir(data_dir) if f.endswith(".csv")])
    all_dataframes = []
    
    for filename in csv_files:
        file_path = os.path.join(data_dir, filename)
        df = pd.read_csv(file_path)
        all_dataframes.append(df)
    
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    return combined_df, csv_files

def preprocess_weather_data(df):
    """날씨 데이터 전처리 통합 함수"""
    # DataFrame 복사
    df = df.copy()
    
    # Date 컬럼을 datetime으로 변환
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    
    # Year, Month, Day 컬럼 추가
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    
    # Precipitation의 'T'(Trace)를 0으로 변환
    df.loc[df["Precipitation"] == "T", "Precipitation"] = 0
    df["Precipitation"] = pd.to_numeric(df["Precipitation"], errors='coerce')
    
    # Snow Depth의 'M'(Missing)을 0으로 변환
    df.loc[df["Snow Depth"] == "M", "Snow Depth"] = 0
    df["Snow Depth"] = pd.to_numeric(df["Snow Depth"], errors='coerce')
    
    # 화씨를 섭씨로 변환
    df["Maximum"] = fahrenheit_to_celsius(df["Maximum"])
    df["Minimum"] = fahrenheit_to_celsius(df["Minimum"])
    df["Average"] = fahrenheit_to_celsius(df["Average"])
    
    # 인치를 mm로 변환
    df["Precipitation"] = inches_to_mm(df["Precipitation"])
    df["Snow Depth"] = inches_to_mm(df["Snow Depth"])
    
    return df

def get_yearly_summary(df):
    """연도별 요약 통계 계산"""
    yearly_summary = df.groupby("Year").agg({
        "Average": "mean",
        "Maximum": "mean", 
        "Minimum": "mean",
        "Precipitation": "sum",
        "Departure": "mean"
    }).reset_index()
    
    return yearly_summary

def get_monthly_summary(df):
    """월별 요약 통계 계산"""
    monthly_summary = df.groupby(["Year", "Month"]).agg({
        "Average": "mean",
        "Maximum": "mean",
        "Minimum": "mean", 
        "Precipitation": "sum",
        "Departure": "mean"
    }).reset_index()
    
    return monthly_summary 
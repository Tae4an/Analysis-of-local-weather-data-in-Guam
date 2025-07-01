"""
괌 날씨 데이터 시각화 모듈
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 한글 폰트 설정 (macOS용)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

def plot_monthly_temperature_by_year(df, save_path=None):
    """연도별 월평균 기온 그래프"""
    monthly_avg_by_year = df.groupby(['Year', 'Month'])['Average'].mean().unstack(level=0)
    
    plt.figure(figsize=(12, 6))
    
    for year in monthly_avg_by_year.columns:
        plt.plot(monthly_avg_by_year.index, monthly_avg_by_year[year], 
                label=str(year), marker='o')
    
    plt.title('연도별 월평균 기온', fontsize=16)
    plt.xlabel('월', fontsize=12)
    plt.ylabel('기온 (°C)', fontsize=12)
    plt.xticks(range(1, 13))
    plt.legend(title='연도')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

def plot_monthly_precipitation_by_year(df, save_path=None):
    """연도별 월평균 강수량 그래프"""
    monthly_precip_by_year = df.groupby(['Year', 'Month'])['Precipitation'].mean().unstack(level=0)
    
    plt.figure(figsize=(12, 6))
    
    for year in monthly_precip_by_year.columns:
        plt.plot(monthly_precip_by_year.index, monthly_precip_by_year[year], 
                label=str(year), marker='o')
    
    plt.title('연도별 월평균 강수량', fontsize=16)
    plt.xlabel('월', fontsize=12)
    plt.ylabel('평균 강수량 (mm)', fontsize=12)
    plt.xticks(range(1, 13))
    plt.legend(title='연도')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

def plot_yearly_summary(df, save_path=None):
    """연간 평균 기온과 총 강수량 그래프"""
    yearly_summary = df.groupby("Year").agg({
        "Average": "mean",
        "Precipitation": "sum"
    }).reset_index()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # 연간 평균 기온
    ax1.plot(yearly_summary["Year"], yearly_summary["Average"], 
             marker='o', linewidth=2, markersize=8, color='red')
    ax1.set_title("연간 평균 기온", fontsize=14)
    ax1.set_xlabel("연도", fontsize=12)
    ax1.set_ylabel("기온 (°C)", fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # 연간 총 강수량
    ax2.bar(yearly_summary["Year"], yearly_summary["Precipitation"], 
            color='skyblue', alpha=0.7)
    ax2.set_title("연간 총 강수량", fontsize=14)
    ax2.set_xlabel("연도", fontsize=12)
    ax2.set_ylabel("강수량 (mm)", fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

def plot_temperature_departure(df, save_path=None):
    """월별 기온 편차 그래프"""
    pivot_departure = df.groupby(["Year", "Month"])["Departure"].mean().unstack(level=0)
    
    plt.figure(figsize=(14, 6))
    
    for year in pivot_departure.columns:
        plt.plot(pivot_departure.index, pivot_departure[year], 
                label=str(year), marker='o')
    
    plt.title("연도별 월별 기온 편차", fontsize=16)
    plt.xlabel("월", fontsize=12)
    plt.ylabel("평년 대비 편차 (°C)", fontsize=12)
    plt.xticks(ticks=range(1, 13))
    plt.axhline(0, color='gray', linestyle='--', alpha=0.7)
    plt.grid(True, alpha=0.3)
    plt.legend(title="연도", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

def plot_forecast_comparison(forecast_df, save_path=None):
    """7일 예보 데이터 시각화"""
    plt.figure(figsize=(12, 6))
    
    plt.plot(forecast_df['Date'], forecast_df['High (°C)'], 
             label='최고 기온 (°C)', marker='o', color='red', linewidth=2)
    plt.plot(forecast_df['Date'], forecast_df['Low (°C)'], 
             label='최저 기온 (°C)', marker='o', color='blue', linewidth=2)
    
    plt.fill_between(forecast_df['Date'], 
                     forecast_df['High (°C)'], 
                     forecast_df['Low (°C)'], 
                     alpha=0.2, color='gray')
    
    plt.xlabel('날짜', fontsize=12)
    plt.ylabel('기온 (°C)', fontsize=12)
    plt.title('괌 7일 기온 예보', fontsize=16)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

def create_comprehensive_dashboard(df, save_path=None):
    """종합 대시보드 생성"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. 연도별 월평균 기온
    monthly_avg_by_year = df.groupby(['Year', 'Month'])['Average'].mean().unstack(level=0)
    for year in monthly_avg_by_year.columns:
        axes[0,0].plot(monthly_avg_by_year.index, monthly_avg_by_year[year], 
                      label=str(year), marker='o')
    axes[0,0].set_title('연도별 월평균 기온')
    axes[0,0].set_xlabel('월')
    axes[0,0].set_ylabel('기온 (°C)')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
    # 2. 연도별 월평균 강수량
    monthly_precip_by_year = df.groupby(['Year', 'Month'])['Precipitation'].mean().unstack(level=0)
    for year in monthly_precip_by_year.columns:
        axes[0,1].plot(monthly_precip_by_year.index, monthly_precip_by_year[year], 
                      label=str(year), marker='o')
    axes[0,1].set_title('연도별 월평균 강수량')
    axes[0,1].set_xlabel('월')
    axes[0,1].set_ylabel('강수량 (mm)')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
    # 3. 연간 평균 기온
    yearly_summary = df.groupby("Year").agg({
        "Average": "mean",
        "Precipitation": "sum"
    }).reset_index()
    
    axes[1,0].plot(yearly_summary["Year"], yearly_summary["Average"], 
                   marker='o', linewidth=2, markersize=8, color='red')
    axes[1,0].set_title('연간 평균 기온')
    axes[1,0].set_xlabel('연도')
    axes[1,0].set_ylabel('기온 (°C)')
    axes[1,0].grid(True, alpha=0.3)
    
    # 4. 연간 총 강수량
    axes[1,1].bar(yearly_summary["Year"], yearly_summary["Precipitation"], 
                  color='skyblue', alpha=0.7)
    axes[1,1].set_title('연간 총 강수량')
    axes[1,1].set_xlabel('연도')
    axes[1,1].set_ylabel('강수량 (mm)')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show() 
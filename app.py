import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 사용자 정의 모듈 import
from src.data_processing import (
    load_all_csv_files, 
    preprocess_weather_data,
    get_yearly_summary,
    get_monthly_summary
)
from src.api_client import get_guam_forecast

# 페이지 설정
st.set_page_config(
    page_title="🌴 괌 날씨 분석 대시보드",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사용자 정의 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #1E88E5 0%, #43A047 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .highlight {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """데이터 로딩 및 전처리"""
    try:
        # CSV 파일들 로드 (tuple에서 DataFrame만 추출)
        df, _ = load_all_csv_files('data')
        df = preprocess_weather_data(df)
        
        # Streamlit 앱에서 기대하는 컬럼명으로 매핑
        df = df.rename(columns={
            'Maximum': 'MaxTemp_C',
            'Minimum': 'MinTemp_C', 
            'Average': 'AvgTemp_C',
            'Precipitation': 'Precipitation_mm'
        })
        
        return df
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
        return pd.DataFrame()

@st.cache_data
def get_api_data():
    """API 데이터 가져오기"""
    try:
        forecast_data = get_guam_forecast()
        if forecast_data is not None:
            # 컬럼명을 표준화
            forecast_data = forecast_data.rename(columns={
                'High (°C)': 'MaxTemp_C',
                'Low (°C)': 'MinTemp_C'
            })
        return forecast_data if forecast_data is not None else pd.DataFrame()
    except Exception as e:
        st.warning(f"실시간 데이터를 가져올 수 없습니다: {e}")
        return pd.DataFrame()

def main():
    # 헤더
    st.markdown('<div class="main-header">🌴 괌 날씨 분석 대시보드</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 데이터 로딩
    with st.spinner('📊 데이터를 로딩 중입니다...'):
        df = load_data()
        
    if df.empty:
        st.error("데이터를 로드할 수 없습니다. data 폴더에 CSV 파일이 있는지 확인해주세요.")
        return
    
    # 사이드바 설정
    st.sidebar.header("🎛️ 대시보드 설정")
    
    # 연도 선택
    available_years = sorted(df['Year'].unique())
    selected_year = st.sidebar.selectbox(
        "📅 분석할 연도 선택", 
        options=['전체'] + available_years,
        index=0
    )
    
    # 월 선택
    selected_month = st.sidebar.selectbox(
        "📆 분석할 월 선택",
        options=['전체'] + list(range(1, 13)),
        index=0,
        format_func=lambda x: f"{x}월" if x != '전체' else '전체'
    )
    
    # 분석 타입 선택
    analysis_type = st.sidebar.selectbox(
        "📈 분석 유형",
        ["전체 개요", "기온 분석", "강수량 분석", "실시간 예보", "기후 변화"]
    )
    
    # 데이터 필터링
    filtered_df = df.copy()
    if selected_year != '전체':
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    if selected_month != '전체':
        filtered_df = filtered_df[filtered_df['Month'] == selected_month]
    
    # 메인 콘텐츠
    if analysis_type == "전체 개요":
        show_overview(filtered_df, df)
    elif analysis_type == "기온 분석":
        show_temperature_analysis(filtered_df)
    elif analysis_type == "강수량 분석":
        show_precipitation_analysis(filtered_df)
    elif analysis_type == "실시간 예보":
        show_forecast_analysis(df)
    elif analysis_type == "기후 변화":
        show_climate_change_analysis(df)

def show_overview(filtered_df, full_df):
    """전체 개요 페이지"""
    st.header("📊 괌 날씨 전체 개요")
    
    # 주요 통계
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_temp = filtered_df['AvgTemp_C'].mean()
        st.metric(
            label="🌡️ 평균 기온",
            value=f"{avg_temp:.1f}°C",
            delta=f"{avg_temp - full_df['AvgTemp_C'].mean():.1f}°C"
        )
    
    with col2:
        total_precip = filtered_df['Precipitation_mm'].sum()
        st.metric(
            label="🌧️ 총 강수량",
            value=f"{total_precip:.0f}mm",
            delta=f"{total_precip - full_df.groupby(['Year', 'Month'])['Precipitation_mm'].sum().mean():.0f}mm"
        )
    
    with col3:
        max_temp = filtered_df['MaxTemp_C'].max()
        st.metric(
            label="🔥 최고 기온",
            value=f"{max_temp:.1f}°C",
            delta=f"{max_temp - full_df['MaxTemp_C'].max():.1f}°C"
        )
    
    with col4:
        min_temp = filtered_df['MinTemp_C'].min()
        st.metric(
            label="❄️ 최저 기온",
            value=f"{min_temp:.1f}°C",
            delta=f"{min_temp - full_df['MinTemp_C'].min():.1f}°C"
        )
    
    st.markdown("---")
    
    # 월별 기온 트렌드
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 월별 기온 변화")
        monthly_temp = filtered_df.groupby('Month')[['AvgTemp_C', 'MaxTemp_C', 'MinTemp_C']].mean().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly_temp['Month'], y=monthly_temp['MaxTemp_C'], 
                                mode='lines+markers', name='최고기온', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=monthly_temp['Month'], y=monthly_temp['AvgTemp_C'], 
                                mode='lines+markers', name='평균기온', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=monthly_temp['Month'], y=monthly_temp['MinTemp_C'], 
                                mode='lines+markers', name='최저기온', line=dict(color='lightblue')))
        
        fig.update_layout(title="월별 기온 변화", xaxis_title="월", yaxis_title="기온 (°C)", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💧 월별 강수량")
        monthly_precip = filtered_df.groupby('Month')['Precipitation_mm'].sum().reset_index()
        
        fig = px.bar(monthly_precip, x='Month', y='Precipitation_mm', 
                    title="월별 총 강수량", color='Precipitation_mm',
                    color_continuous_scale='Blues')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # 연도별 비교 (전체 데이터가 있을 때만)
    if len(full_df['Year'].unique()) > 1:
        st.subheader("📅 연도별 기후 비교")
        yearly_summary = full_df.groupby('Year').agg({
            'AvgTemp_C': 'mean',
            'Precipitation_mm': 'sum'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(yearly_summary, x='Year', y='AvgTemp_C', 
                         title="연도별 평균 기온 변화", markers=True)
            fig.update_layout(yaxis_title="평균 기온 (°C)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(yearly_summary, x='Year', y='Precipitation_mm', 
                        title="연도별 총 강수량", color='Precipitation_mm',
                        color_continuous_scale='Blues')
            fig.update_layout(yaxis_title="총 강수량 (mm)")
            st.plotly_chart(fig, use_container_width=True)

def show_temperature_analysis(df):
    """기온 분석 페이지"""
    st.header("🌡️ 기온 상세 분석")
    
    # 기온 분포
    st.subheader("📊 기온 분포")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(df, x='AvgTemp_C', nbins=30, title="평균 기온 분포",
                          color_discrete_sequence=['skyblue'])
        fig.update_layout(xaxis_title="평균 기온 (°C)", yaxis_title="빈도")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(df, y='AvgTemp_C', title="평균 기온 박스플롯")
        st.plotly_chart(fig, use_container_width=True)
    
    # 기온 범위 분석
    st.subheader("📏 기온 범위 분석")
    df['TempRange'] = df['MaxTemp_C'] - df['MinTemp_C']
    
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_range = df.groupby('Month')['TempRange'].mean().reset_index()
        fig = px.bar(monthly_range, x='Month', y='TempRange', 
                    title="월별 평균 일교차", color='TempRange',
                    color_continuous_scale='Reds')
        fig.update_layout(xaxis_title="월", yaxis_title="일교차 (°C)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 기온 극값 분석
        temp_extremes = pd.DataFrame({
            '구분': ['최고 기온', '최저 기온', '최대 일교차'],
            '값': [df['MaxTemp_C'].max(), df['MinTemp_C'].min(), df['TempRange'].max()],
            '단위': ['°C', '°C', '°C']
        })
        
        fig = px.bar(temp_extremes, x='구분', y='값', text='값',
                    title="기온 극값", color='구분')
        fig.update_traces(texttemplate='%{text:.1f}°C', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

def show_precipitation_analysis(df):
    """강수량 분석 페이지"""
    st.header("🌧️ 강수량 상세 분석")
    
    # 강수 패턴
    st.subheader("💧 강수 패턴 분석")
    
    # 강수일 vs 무강수일
    rainy_days = (df['Precipitation_mm'] > 0).sum()
    total_days = len(df)
    dry_days = total_days - rainy_days
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🌧️ 강수일", f"{rainy_days}일", f"{(rainy_days/total_days)*100:.1f}%")
    
    with col2:
        st.metric("☀️ 무강수일", f"{dry_days}일", f"{(dry_days/total_days)*100:.1f}%")
    
    with col3:
        avg_precip = df[df['Precipitation_mm'] > 0]['Precipitation_mm'].mean()
        st.metric("💧 평균 강수량", f"{avg_precip:.1f}mm", "(강수일 기준)")
    
    # 강수량 분포
    col1, col2 = st.columns(2)
    
    with col1:
        # 강수량 범주별 분류
        df['PrecipCategory'] = pd.cut(df['Precipitation_mm'], 
                                     bins=[0, 1, 10, 50, float('inf')],
                                     labels=['무강수', '약한비', '보통비', '강한비'])
        precip_counts = df['PrecipCategory'].value_counts()
        
        fig = px.pie(values=precip_counts.values, names=precip_counts.index,
                    title="강수량 범주별 분포")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 월별 강수 패턴
        monthly_precip = df.groupby('Month')['Precipitation_mm'].agg(['sum', 'mean', 'count']).reset_index()
        monthly_precip.columns = ['Month', 'Total', 'Average', 'Count']
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=monthly_precip['Month'], y=monthly_precip['Total'], 
                            name='총 강수량', marker_color='lightblue'), secondary_y=False)
        fig.add_trace(go.Scatter(x=monthly_precip['Month'], y=monthly_precip['Average'], 
                                mode='lines+markers', name='평균 강수량', line=dict(color='red')), secondary_y=True)
        
        fig.update_xaxes(title_text="월")
        fig.update_yaxes(title_text="총 강수량 (mm)", secondary_y=False)
        fig.update_yaxes(title_text="평균 강수량 (mm)", secondary_y=True)
        fig.update_layout(title_text="월별 강수량 패턴")
        
        st.plotly_chart(fig, use_container_width=True)

def show_forecast_analysis(df):
    """실시간 예보 분석 페이지"""
    st.header("🔮 실시간 날씨 예보")
    
    # API 데이터 가져오기
    with st.spinner('🌐 실시간 데이터를 가져오는 중...'):
        forecast_df = get_api_data()
    
    if not forecast_df.empty:
        st.success("✅ 실시간 데이터를 성공적으로 가져왔습니다!")
        
        # 예보 요약
        st.subheader("📋 7일 예보 요약")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_high = forecast_df['MaxTemp_C'].mean()
            st.metric("🔥 평균 최고기온", f"{avg_high:.1f}°C")
        
        with col2:
            avg_low = forecast_df['MinTemp_C'].mean()
            st.metric("❄️ 평균 최저기온", f"{avg_low:.1f}°C")
        
        with col3:
            temp_range = forecast_df['MaxTemp_C'].mean() - forecast_df['MinTemp_C'].mean()
            st.metric("📏 평균 일교차", f"{temp_range:.1f}°C")
        
        with col4:
            if 'Precipitation_mm' in forecast_df.columns:
                total_precip = forecast_df['Precipitation_mm'].sum()
                st.metric("🌧️ 예상 강수량", f"{total_precip:.1f}mm")
            else:
                st.metric("🌧️ 강수 정보", "데이터 없음")
        
        # 예보 차트
        st.subheader("📈 7일 기온 예보")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['MaxTemp_C'],
                                mode='lines+markers', name='최고기온', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['MinTemp_C'],
                                mode='lines+markers', name='최저기온', line=dict(color='blue')))
        
        fig.update_layout(title="7일 기온 예보", xaxis_title="날짜", yaxis_title="기온 (°C)")
        st.plotly_chart(fig, use_container_width=True)
        
        # 과거 데이터와 비교
        st.subheader("🔍 과거 데이터와 비교")
        
        # 현재 월의 과거 평균 계산
        current_month = datetime.now().month
        historical_data = df[df['Month'] == current_month]
        
        if not historical_data.empty:
            hist_avg_max = historical_data['MaxTemp_C'].mean()
            hist_avg_min = historical_data['MinTemp_C'].mean()
            forecast_avg_max = forecast_df['MaxTemp_C'].mean()
            forecast_avg_min = forecast_df['MinTemp_C'].mean()
            
            comparison_data = pd.DataFrame({
                '구분': ['과거 평균 최고기온', '예보 평균 최고기온', '과거 평균 최저기온', '예보 평균 최저기온'],
                '기온': [hist_avg_max, forecast_avg_max, hist_avg_min, forecast_avg_min],
                '타입': ['과거', '예보', '과거', '예보']
            })
            
            fig = px.bar(comparison_data, x='구분', y='기온', color='타입',
                        title=f"{current_month}월 과거 평균 vs 현재 예보", 
                        text='기온')
            fig.update_traces(texttemplate='%{text:.1f}°C', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        # 예보 상세 테이블
        st.subheader("📅 상세 예보 정보")
        st.dataframe(forecast_df, use_container_width=True)
        
    else:
        st.warning("⚠️ 실시간 예보 데이터를 가져올 수 없습니다.")
        st.info("💡 과거 데이터를 기반으로 한 통계적 예측을 표시합니다.")
        
        # 통계적 예측 (과거 데이터 기반)
        current_month = datetime.now().month
        historical_data = df[df['Month'] == current_month]
        
        if not historical_data.empty:
            st.subheader(f"📊 {current_month}월 통계 기반 예측")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🌡️ 예상 평균기온", 
                         f"{historical_data['AvgTemp_C'].mean():.1f}°C",
                         f"±{historical_data['AvgTemp_C'].std():.1f}")
            
            with col2:
                st.metric("🔥 예상 최고기온", 
                         f"{historical_data['MaxTemp_C'].mean():.1f}°C",
                         f"±{historical_data['MaxTemp_C'].std():.1f}")
            
            with col3:
                st.metric("❄️ 예상 최저기온", 
                         f"{historical_data['MinTemp_C'].mean():.1f}°C",
                         f"±{historical_data['MinTemp_C'].std():.1f}")

def show_climate_change_analysis(df):
    """기후 변화 분석 페이지"""
    st.header("🌍 기후 변화 트렌드")
    
    # 연도별 트렌드
    yearly_data = df.groupby('Year').agg({
        'AvgTemp_C': 'mean',
        'MaxTemp_C': 'mean',
        'MinTemp_C': 'mean',
        'Precipitation_mm': 'sum'
    }).reset_index()
    
    # 기온 트렌드
    st.subheader("📈 기온 변화 트렌드")
    
    fig = make_subplots(rows=2, cols=2,
                       subplot_titles=("평균 기온", "최고 기온", "최저 기온", "연간 강수량"))
    
    # 평균 기온
    fig.add_trace(go.Scatter(x=yearly_data['Year'], y=yearly_data['AvgTemp_C'],
                            mode='lines+markers', name='평균기온'), row=1, col=1)
    
    # 최고 기온
    fig.add_trace(go.Scatter(x=yearly_data['Year'], y=yearly_data['MaxTemp_C'],
                            mode='lines+markers', name='최고기온', line=dict(color='red')), row=1, col=2)
    
    # 최저 기온
    fig.add_trace(go.Scatter(x=yearly_data['Year'], y=yearly_data['MinTemp_C'],
                            mode='lines+markers', name='최저기온', line=dict(color='blue')), row=2, col=1)
    
    # 강수량
    fig.add_trace(go.Bar(x=yearly_data['Year'], y=yearly_data['Precipitation_mm'],
                        name='연간강수량', marker=dict(color='lightblue')), row=2, col=2)
    
    fig.update_layout(height=600, showlegend=False, title_text="연도별 기후 변화")
    st.plotly_chart(fig, use_container_width=True)
    
    # 트렌드 분석
    st.subheader("📊 트렌드 분석 결과")
    
    # 선형 회귀로 트렌드 계산
    years = yearly_data['Year'].values.reshape(-1, 1)
    
    from sklearn.linear_model import LinearRegression
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌡️ 기온 트렌드")
        
        # 평균 기온 트렌드
        lr_temp = LinearRegression().fit(years, yearly_data['AvgTemp_C'])
        temp_slope = lr_temp.coef_[0]
        
        if temp_slope > 0:
            st.success(f"📈 평균 기온 상승 추세: **+{temp_slope:.3f}°C/년**")
        else:
            st.info(f"📉 평균 기온 하락 추세: **{temp_slope:.3f}°C/년**")
        
        # 기온 변동성
        temp_std = yearly_data['AvgTemp_C'].std()
        st.info(f"🔄 연간 기온 변동성: **±{temp_std:.2f}°C**")
    
    with col2:
        st.markdown("#### 💧 강수량 트렌드")
        
        # 강수량 트렌드
        lr_precip = LinearRegression().fit(years, yearly_data['Precipitation_mm'])
        precip_slope = lr_precip.coef_[0]
        
        if precip_slope > 0:
            st.success(f"📈 강수량 증가 추세: **+{precip_slope:.1f}mm/년**")
        else:
            st.info(f"📉 강수량 감소 추세: **{precip_slope:.1f}mm/년**")
        
        # 강수량 변동성
        precip_std = yearly_data['Precipitation_mm'].std()
        st.info(f"🔄 연간 강수량 변동성: **±{precip_std:.0f}mm**")
    
    # 이상 기후 탐지
    st.subheader("⚠️ 이상 기후 탐지")
    
    # Z-score 기반 이상치 탐지
    from scipy import stats
    
    df['TempZScore'] = np.abs(stats.zscore(df['AvgTemp_C']))
    df['PrecipZScore'] = np.abs(stats.zscore(df['Precipitation_mm']))
    
    # 이상치 (Z-score > 2)
    temp_outliers = df[df['TempZScore'] > 2]
    precip_outliers = df[df['PrecipZScore'] > 2]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌡️ 이상 기온 기록")
        if not temp_outliers.empty:
            for _, row in temp_outliers.iterrows():
                if row['AvgTemp_C'] > df['AvgTemp_C'].mean():
                    st.error(f"🔥 {row['Year']}-{row['Month']:02d}: {row['AvgTemp_C']:.1f}°C (평균 대비 +{row['AvgTemp_C'] - df['AvgTemp_C'].mean():.1f}°C)")
                else:
                    st.info(f"❄️ {row['Year']}-{row['Month']:02d}: {row['AvgTemp_C']:.1f}°C (평균 대비 {row['AvgTemp_C'] - df['AvgTemp_C'].mean():.1f}°C)")
        else:
            st.success("✅ 이상 기온 기록 없음")
    
    with col2:
        st.markdown("#### 💧 이상 강수량 기록")
        if not precip_outliers.empty:
            for _, row in precip_outliers.iterrows():
                if row['Precipitation_mm'] > df['Precipitation_mm'].mean():
                    st.warning(f"🌧️ {row['Year']}-{row['Month']:02d}: {row['Precipitation_mm']:.1f}mm (평균 대비 +{row['Precipitation_mm'] - df['Precipitation_mm'].mean():.1f}mm)")
                else:
                    st.info(f"☀️ {row['Year']}-{row['Month']:02d}: {row['Precipitation_mm']:.1f}mm (평균 대비 {row['Precipitation_mm'] - df['Precipitation_mm'].mean():.1f}mm)")
        else:
            st.success("✅ 이상 강수량 기록 없음")

if __name__ == "__main__":
    main() 
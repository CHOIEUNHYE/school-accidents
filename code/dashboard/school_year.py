# 연도별 분석 streamlit 파일
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu
import pandas as pd
import polars as pl
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import matplotlib.pyplot as plt
import json
import os
from function_year_region import *  # function_year_region.py 파일에서 모든 함수 불러오기 


# 현재 파일의 디렉토리를 기준으로 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))

# 폰트 설정
with open( current_dir+"/component/style/KoPubWorld Dotum.css" ) as css:
    st.write( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

with open( current_dir+"/component/style/style.css" ) as css:
    st.write( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


#######################
#데이터 불러오기
df = pl.read_csv('../../../school-accidents/code/dashboard/dashboard_data/학교안전사고데이터통합/학교안전사고데이터_5개년통합_월계절추가.csv')
df = df.to_pandas()
df['사고발생일'] = pd.to_datetime(df['사고발생일'])
df['연도'] = df['사고발생일'].map(lambda x : x.year)

# 데이터 전처리
df_2019 = df[df['사고발생일'].between('2019-01-01', '2019-12-31')]
df_2020 = df[df['사고발생일'].between('2020-01-01', '2020-12-31')]
df_2021 = df[df['사고발생일'].between('2021-01-01', '2021-12-31')]
df_2022 = df[df['사고발생일'].between('2022-01-01', '2022-12-31')]
df_2023 = df[df['사고발생일'].between('2023-01-01', '2023-12-31')]
# 각 연도별 데이터프레임 리스트
dataframes = [df_2019, df_2020, df_2021, df_2022, df_2023]
years = [2019, 2020, 2021, 2022, 2023]

#######################
st.markdown('''
    <h1 style="font-family: 'KoPubWorld Dotum', sans-serif; text-align: center;">
        학교안전사고 분석
    </h1>
    ''', unsafe_allow_html=True)

st.write("2019년~2023년 5년간의 학교 안전 사고 데이터를 통해 관련 현황을 분석하고, 유형을 분류하여 학교 안전 사고 예방을 위한 인사이트를 도출합니다. 지역, 학교급, 사고 내용을 기준으로 데이터를 분류하여 세부 분석을 진행하였습니다. 각 분석에 대한 내용은 사이드 바의 탭을 통해 확인할 수 있습니다.")
st.write("")


# 레이아웃 나누기
col = st.columns((4.5, 1.5), gap='medium')

with col[0] :
    st.markdown('#### 연도별 사고 발생 현황 ') 
    # 탭 추가
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['5개년 통합', '2019년', '2020년', '2021년', '2022년', '2023년'])
        
    # 5개년 통합
    with tab1:
        # 월별 사고 건수 집계하는 함수
        def monthly_counts(df):
            df['사고발생일'] = pd.to_datetime(df['사고발생일'])
            df['월'] = df['사고발생일'].dt.to_period('M').dt.to_timestamp()
            return df['월'].value_counts().sort_index().reset_index()
            
        # 모든 연도별 월별 사고 건수 집계
        all_data_monthly = pd.DataFrame()
        for df, year in zip(dataframes, years):
            monthly_counts_df = monthly_counts(df)
            monthly_counts_df.columns = ['월', '사고 건수']
            monthly_counts_df['연도'] = year
            all_data_monthly = pd.concat([all_data_monthly, monthly_counts_df])
        # 색상 팔레트 및 컬러 맵 설정
        palette = ["#92b8ff", "#aeceff", '#c3b7eb', '#9590e6', '#837ed5']
        color_discrete_map = {str(year): color for year, color in zip(years, palette)}
            
        all_data_monthly['연도'] = all_data_monthly['연도'].astype(str)
            
        # 그래프 생성
        fig = px.bar(all_data_monthly, x='월', y='사고 건수', color='연도', 
        labels={'연도-월': '연도-월', '사고 건수': '사고 건수', '연도': '연도'}, 
        color_discrete_map=color_discrete_map)
            
        fig.update_layout(
            font=dict(family='KoPubWorld돋움체 Medium', color='black'),
            hoverlabel=dict(font_size=15, font_family="KoPubWorld돋움체 Medium"),
            paper_bgcolor='white', plot_bgcolor='white', yaxis=dict(tickformat=','))
            
        fig.update_traces(
            hovertemplate='<b><br>%{x}</b></br>건수: %{y}<br><extra></extra>')
            
        # 그래프 출력
        st.plotly_chart(fig)





    # 연도별 월별 사고 건수 
    def plot_monthly_accidents(df, year, color):
        df_year = df[df['사고발생일'].dt.year == year].copy()
        df_year['월'] = df_year['사고발생일'].dt.month
        yearly_counts = df_year['월'].value_counts().sort_index()
            
        fig = px.bar(yearly_counts, x=yearly_counts.index, y=yearly_counts.values,
                 labels={'x': '월', 'y': '사고 건수'}, color_discrete_sequence=[color])
        fig.update_layout(
            font=dict({'family':'KoPubWorld돋움체_Pro','color':'black'}),
            hoverlabel=dict(font_size=15, font_family="KoPubWorld돋움체_Pro"),
            paper_bgcolor='white',
            plot_bgcolor='white', 
            yaxis=dict(tickformat=',', title='사고 건수'))
        fig.update_traces(
            hovertemplate='<b><br>%{x}월</b></br>건수: %{y}<br><extra></extra>')
        return fig
        
    monthly_counts2019 = plot_monthly_accidents(df_2019, 2019, '#92b8ff')
    monthly_counts2020 = plot_monthly_accidents(df_2020, 2020, '#aeceff')
    monthly_counts2021 = plot_monthly_accidents(df_2021, 2021, '#c3b7eb')
    monthly_counts2022 = plot_monthly_accidents(df_2022, 2022, '#9590e6')
    monthly_counts2023 = plot_monthly_accidents(df_2023, 2023, '#837ed5')

    # 2019년
    with tab2:
        st.plotly_chart(monthly_counts2019)
    # 2020년
    with tab3:
        st.plotly_chart(monthly_counts2020)
    # 2021년
    with tab4:
        st.plotly_chart(monthly_counts2021)
    # 2022년
    with tab5:
        st.plotly_chart(monthly_counts2022)
    # 2023년
    with tab6:
        st.plotly_chart(monthly_counts2023)





with col[1]:
    st.markdown('#### 연도별 총 사고 건수 ') 

    st.divider()
    
    # 연도별 사고 건수 집계
    yearly_counts = pd.DataFrame({'연도': years})
    # 각 연도별 데이터프레임에서 사고 건수 계산
    for df_year, year in zip(dataframes, years):
        yearly_counts.loc[yearly_counts['연도'] == year, '사고 건수'] = len(df_year)
    yearly_counts['연도'] = yearly_counts['연도'].astype(str)
    yearly_counts['사고 건수'] = yearly_counts['사고 건수'].astype(int)

    # 데이터프레임 표시
    for index, row in yearly_counts.iterrows():
        year = row['연도']
        count = row['사고 건수']

        
        st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin: 0; padding: 0; width: 150px;">
                <p style="margin: 0; padding: 0; font-size: 15px; font-weight: bold; width: 75px; text-align: left;">{year}년</p>
                <p style="margin: 0; padding: 0; font-size: 14px; width: 75px; text-align: center;">{count:,}건</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

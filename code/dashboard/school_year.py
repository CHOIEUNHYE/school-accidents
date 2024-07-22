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
from function_하윤 import *  # function.py 파일에서 모든 함수 불러오기 


def run_year(df):
    # 데이터 전처리
    df_2019 = df[df['사고발생일'].between('2019-01-01', '2019-12-31')]
    df_2020 = df[df['사고발생일'].between('2020-01-01', '2020-12-31')]
    df_2021 = df[df['사고발생일'].between('2021-01-01', '2021-12-31')]
    df_2022 = df[df['사고발생일'].between('2022-01-01', '2022-12-31')]
    df_2023 = df[df['사고발생일'].between('2023-01-01', '2023-12-31')]
    # 각 연도별 데이터프레임 리스트
    dataframes = [df_2019, df_2020, df_2021, df_2022, df_2023]
    years = [2019, 2020, 2021, 2022, 2023]



    st.title('연도별 사고 현황 분석')
    st.write("설명")



    # 레이아웃 나누기
    col = st.columns((4.5, 1.5), gap='medium')

    with col[0] :
        st.markdown('#### 사고 발생 현황 ') 
        # 탭 추가
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['5년 통합', '2019년', '2020년', '2021년', '2022년', '2023년'])
        
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



            # 연도별 월별 heatmap 생성
            def monthly_counts2(df):
                df['사고발생일'] = pd.to_datetime(df['사고발생일'])
                return df.groupby(df['사고발생일'].dt.month).size().reset_index(name='사고 건수')
            
            monthly_counts_list = [monthly_counts2(df).rename(columns={'사고 건수': year}) for df, year in zip(dataframes, years)]

            merged_df = pd.concat(monthly_counts_list, axis=1, join='outer')
            merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

            merged_df = merged_df.set_index('사고발생일')
            merged_df.index = merged_df.index.map(lambda x: f'{x}월')
            merged_df = merged_df.fillna(0)
            colorscale = [[0, '#F7FBFC'], [0.2, '#E6F3F9'], [0.4, '#D6E6F2'], [0.6, '#B9D7EA'], [0.8, '#A2C5E2'], [1, '#769FCD']]

            fig = go.Figure(data=go.Heatmap(
                   z=merged_df.values, x=merged_df.columns, y=merged_df.index[::-1],
                   colorscale=colorscale, text=merged_df.values, texttemplate="%{z:,.0f}",
                   hovertemplate='<b>%{x}년 %{y}</b><br>사고 건수: %{z:,.0f} 건<extra></extra>',))
            fig.update_layout(font=dict(family="KoPubWorld돋움체_Pro", size=12))

            # 그래프 출력
            st.markdown('#### 연도별 월별 사고 발생 현황 ') 
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
        
        # 연도별 사고 현황 분석
        def month_analysis(year_df):
            st.markdown('##### 사고 시간과 사고 장소 ')
            st.write("파이차트 크기 수정이 필요...")
            col = st.columns([3,3], gap='medium')
            with col[0] :
                create_pie_chart(count_to(year_df['사고시간']), '사고시간')
            with col[1] :
                create_pie_chart(count_to(year_df['사고장소']), '사고장소')

            st.markdown('##')

            st.markdown('##### 사고 부위와 형태 ')
            col = st.columns([3,3], gap='medium')
            with col[0] :
                create_pie_chart(count_to(year_df['사고부위']), '사고부위')
            with col[1] :
                create_pie_chart(count_to(year_df['사고형태']), '사고형태')

            st.markdown('##')

            st.markdown('##### 사고 당시 활동과 매개물 ')
            col = st.columns([3,3], gap='medium')
            with col[0] :
                create_pie_chart(count_to(year_df['사고당시활동']), '사고당시활동')
            with col[1] :
                create_pie_chart(count_to(year_df['사고매개물'].str.split('(').str[0]), '사고매개물')
            

        # 2019년
        with tab2:
            st.plotly_chart(monthly_counts2019)
            st.markdown('##')
            month_analysis(df_2019)
        # 2020년
        with tab3:
            st.plotly_chart(monthly_counts2020)
            st.markdown('##')
            month_analysis(df_2020)
        # 2021년
        with tab4:
            st.plotly_chart(monthly_counts2021)
            st.markdown('##')
            month_analysis(df_2021)
        # 2022년
        with tab5:
            st.plotly_chart(monthly_counts2022)
            st.markdown('##')
            month_analysis(df_2022)
        # 2023년
        with tab6:
            st.plotly_chart(monthly_counts2023)
            st.markdown('##')
            month_analysis(df_2023)





    with col[1]:
        st.markdown('#### 연도별 총 사고 건수 ') 
        # 연도별 사고 건수 집계
        yearly_counts = pd.DataFrame({'연도': years})
        # 각 연도별 데이터프레임에서 사고 건수 계산
        for df_year, year in zip(dataframes, years):
            yearly_counts.loc[yearly_counts['연도'] == year, '사고 건수'] = len(df_year)
        yearly_counts['연도'] = yearly_counts['연도'].astype(str)
        yearly_counts['사고 건수'] = yearly_counts['사고 건수'].astype(int)

        # 데이터프레임 표시
        st.dataframe(yearly_counts[['연도','사고 건수']], hide_index=True)
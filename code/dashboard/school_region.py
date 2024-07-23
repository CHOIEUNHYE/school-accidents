# 지역별 분석 streamlit 파일
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

# geojson파일 불러오기
file_path = '../../data/지도 시각화 데이터\TL_SCCO_CTPRVN.json'
geojson = gpd.read_file(file_path)
geojson = geojson.replace('강원도','강원특별자치도') # 강원도 표기 변경
geojson['지역'] = geojson['CTP_KOR_NM'].apply(extract_region) # 학교 안전사고 데이터와 지역 표기 형식 맞추기(충청남도->충북)
geojson_loads = json.loads(geojson.to_json()) # geojson 데이터프레임을 json 형식으로

# 지도 생성
def create_map(df, location_column, parameter_column):
    color_scale = ['#F7FBFC', '#769FCD']

    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations=location_column,
        featureidkey="properties." + location_column,
        color=parameter_column,
        color_continuous_scale=color_scale,
        mapbox_style="white-bg",
        zoom=5.5,
        center={"lat": 36.5, "lon": 127.5},
        opacity=0.5,
        labels={parameter_column: parameter_column}
    )
    
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        font=dict({'family':'KoPubWorld돋움체 Medium','color':'black'}), 
        hoverlabel=dict(font_size=15, font_family="KoPubWorld돋움체 Medium"),
        yaxis=dict(tickformat=','),
        showlegend=False 
    )

    return st.plotly_chart(fig)

# 학교별 데이터 불러오기 - 시도별
school2019 = pd.ExcelFile('../../data/학교,학과별 데이터셋_전처리/2019년_상반기_시도별.xlsx')
school2020 = pd.ExcelFile('../../data/학교,학과별 데이터셋_전처리/2020년_상반기_시도별.xlsx')
school2021 = pd.ExcelFile('../../data/학교,학과별 데이터셋_전처리/2021년_상반기_시도별.xlsx')
school2022 = pd.ExcelFile('../../data/학교,학과별 데이터셋_전처리/2022년_상반기_시도별.xlsx')
school2023 = pd.ExcelFile('../../data/학교,학과별 데이터셋_전처리/2023년_상반기_시도별.xlsx')

# 학교별 데이터 연도별 데이터 프레임 생성 - 시도별
school2019_df = schooldf1(school2019)
school2020_df = schooldf1(school2020)
school2021_df = schooldf1(school2021)
school2022_df = schooldf1(school2022)
school2023_df = schooldf1(school2023)



def run_region(df):
    # 데이터 전처리
    df_2019 = df[df['사고발생일'].between('2019-01-01', '2019-12-31')]
    df_2020 = df[df['사고발생일'].between('2020-01-01', '2020-12-31')]
    df_2021 = df[df['사고발생일'].between('2021-01-01', '2021-12-31')]
    df_2022 = df[df['사고발생일'].between('2022-01-01', '2022-12-31')]
    df_2023 = df[df['사고발생일'].between('2023-01-01', '2023-12-31')]

    # 학교별 데이터 연도별 데이터 프레임 생성 - 시도별
    school2019_df = schooldf1(school2019)
    school2020_df = schooldf1(school2020)
    school2021_df = schooldf1(school2021)
    school2022_df = schooldf1(school2022)
    school2023_df = schooldf1(school2023)

    # 시도별 전체 건수 데이터
    CTPRVN_count = count_to(df['지역'])
    CTPRVN_count_geo = geojson.merge(CTPRVN_count, on='지역')

    # 연도별 건수
    geodf2019 = count_to(df_2019['지역'])
    geodf2019['연도'] = '2019'
    geodf2020 = count_to(df_2020['지역'])
    geodf2020['연도'] = '2020'
    geodf2021 = count_to(df_2021['지역'])
    geodf2021['연도'] = '2021'
    geodf2022 = count_to(df_2022['지역'])
    geodf2022['연도'] = '2022'
    geodf2023 = count_to(df_2023['지역'])
    geodf2023['연도'] = '2023'

    # 연도별 평균 건수
    CTPRVN_2019 = geodf2019.merge(school2019_df, on='지역')
    CTPRVN_2019['사고건수/학생수'] = CTPRVN_2019['건수']/CTPRVN_2019['학생수']
    CTPRVN_2020 = geodf2020.merge(school2020_df, on='지역')
    CTPRVN_2020['사고건수/학생수'] = CTPRVN_2020['건수']/CTPRVN_2020['학생수']
    CTPRVN_2021 = geodf2021.merge(school2021_df, on='지역')
    CTPRVN_2021['사고건수/학생수'] = CTPRVN_2021['건수']/CTPRVN_2021['학생수']
    CTPRVN_2022 = geodf2021.merge(school2021_df, on='지역')
    CTPRVN_2022['사고건수/학생수'] = CTPRVN_2022['건수']/CTPRVN_2022['학생수']
    CTPRVN_2023 = geodf2021.merge(school2021_df, on='지역')
    CTPRVN_2023['사고건수/학생수'] = CTPRVN_2023['건수']/CTPRVN_2023['학생수']





    st.markdown('''
    <h2 style="font-family: 'KoPubWorld Dotum', sans-serif;">
        지역별 안전사고 발생 현황
    </h2>
    ''', unsafe_allow_html=True)


    # 레이아웃 나누기
    col = st.columns((4.5, 1.5), gap='medium')



    # 탭 만들기
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["5개년 통합","2019년", "2020년", "2021년", "2022년","2023년"])

    with tab1:
        col = st.columns((1.5, 4.5), gap='medium')
        with col[0]:
            st.markdown('#### 지역별 사고 건수 ')
            create_chart(CTPRVN_count, '지역')
            
        with col[1]:
            st.markdown('####')
            create_map(CTPRVN_count_geo, '지역', '건수')  
            


    with tab2:
        col = st.columns((1.5, 4.5), gap='medium')
        with col[0]:
            st.markdown('#### 2019년 지역별 사고 건수 ')
            create_chart(geodf2019, '지역')
        
        with col[1]:
            st.markdown('#### 2019년 지역별 학생 수 대비 사고 건수')
            create_map(CTPRVN_2019, '지역', '사고건수/학생수')
            
    

    with tab3:
        col = st.columns((4.5, 1.5), gap='medium')
        with col[0]:
            st.markdown('#### 2020년 지역별 학생 수 대비 사고 건수')
            create_map(CTPRVN_2020, '지역', '사고건수/학생수')
        
        with col[1]:
            st.markdown('#### 2020년 지역별 사고 건수 ')
            create_chart(geodf2020, '지역')


    with tab4:
        col = st.columns((4.5, 1.5), gap='medium')
        with col[0]:
            st.markdown('#### 2021년 지역별 학생 수 대비 사고 건수')
            create_map(CTPRVN_2021, '지역', '사고건수/학생수')
        with col[1]:
            st.markdown('#### 2021년 지역별 사고 건수 ')
            create_chart2(geodf2021, '지역')



    with tab5:
        col = st.columns((4.5, 1.5), gap='medium')
        with col[0]:
            st.markdown('#### 2022년 지역별 학생 수 대비 사고 건수')
            create_map(CTPRVN_2022, '지역', '사고건수/학생수')
        with col[1]:
            st.markdown('#### 2022년 지역별 사고 건수 ')
            create_chart2(geodf2022, '지역')



    with tab6:
        col = st.columns((1.5, 4.5), gap='medium')
        with col[0]:
            st.markdown('#### 2023년 지역별 사고 건수 ')
            create_chart(geodf2023, '지역')
        
        with col[1]:
            st.markdown('#### 2023년 지역별 학생 수 대비 사고 건수')
            create_map(CTPRVN_2023, '지역', '사고건수/학생수')


    st.divider()

    # 처리할 지역 목록
    regions = df['지역'].unique()
    region_results = {}

    # 각 지역별로 데이터 필터링 및 처리
    for region in regions:
        region_df = df[df['지역'] == region]
        processed_data = count_to(region_df['교육청'])
        processed_data['교육청'] = processed_data['교육청'].str.replace('교육지원청', '', regex=False)
        region_results[region] = processed_data
    
    # 탭 만들기
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["서울","부산", "대구", "인천", "대전","광주", "울산"])

    with tab1:
        create_chart(region_results['서울'], '교육청')
    with tab2:
        create_chart(region_results['부산'], '교육청')
    with tab3:
        create_chart(region_results['대구'], '교육청')
    with tab4:
        create_chart(region_results['인천'], '교육청')

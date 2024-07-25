# 지역별 분석 streamlit 파일
import streamlit as st
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
df = pl.read_csv(current_dir +'/component/data/학교안전사고데이터통합/학교안전사고데이터_5개년통합_월계절추가.csv')
df = df.to_pandas()
df['사고발생일'] = pd.to_datetime(df['사고발생일'])
df['연도'] = df['사고발생일'].map(lambda x : x.year)


# geojson파일 불러오기
file_path = '/../../data/지도 시각화 데이터\TL_SCCO_CTPRVN.json'
geojson = gpd.read_file(file_path)
geojson = geojson.replace('강원도','강원특별자치도') # 강원도 표기 변경
geojson['지역'] = geojson['CTP_KOR_NM'].apply(extract_region) # 학교 안전사고 데이터와 지역 표기 형식 맞추기(충청남도->충북)
geojson_loads = json.loads(geojson.to_json()) # geojson 데이터프레임을 json 형식으로

# 지도 생성 함수 설정
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

#######################


st.markdown('''
    <h1 style="font-family: 'KoPubWorld Dotum', sans-serif; text-align: center;">
        학교안전사고 지역별 분석
    </h1>
    ''', unsafe_allow_html=True)

st.write('2019년~2023년 5개년간의 지역별 안전사고 발생 현황에 대한 정보를 제공합니다. 시도별 사고 현황을 연도별로 분석하고, 각 시도별 관할 교육(지원)청에 따라 세부 분석을 진행하였습니다.')


# 레이아웃 나누기
col = st.columns((4.5, 1.5), gap='medium')



# 탭 만들기
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["5개년 통합","2019년", "2020년", "2021년", "2022년","2023년"])

region_count = df.groupby(['연도', '지역']).agg(총사고수=('사고발생일', 'count')).reset_index()
region_count['지역'] = pd.Categorical(region_count['지역'])
region_count = region_count.sort_values(['연도', '지역']).reset_index(drop=True)
region_count['전년대비증감률'] = region_count.groupby('지역')['총사고수'].pct_change().fillna(0) * 100

with tab1:
    st.markdown('#### 지역별 사고 건수 ')
    col = st.columns((2, 1, 3), gap='medium')
       
    with col[0]: 
        create_chart(CTPRVN_count, '지역')
    with col[1]:

        for index, row in CTPRVN_count.iterrows():
            region = row['지역']
            count = row['건수']
            rate = row['퍼센트(%)']
                
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin: 0; padding: 0; width: 150px;">
                <p style="margin: 0; padding: 0; font-size: 15px; font-weight: bold; width: 50px; text-align: left;">{region}</p>
                <p style="margin: 0; padding: 0; font-size: 14px; width: 50px; text-align: center;">{count}</p>
                <p style="margin: 0; padding: 0; font-size: 8px; width: 50px; text-align: right; color: 'grey';"> {rate:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)
            
    with col[2]:
        create_map(CTPRVN_count_geo, '지역', '건수')  


# 연도별 탭 구성
def display_year_tab(year, yeardf, mapdf):
    col = st.columns((2, 1, 3), gap='medium')

    with col[0]:
        st.markdown(f'#### {year}년 지역별 사고 건수 ')
        create_chart(count_to(yeardf['지역']), '지역')
        
    with col[1]:
        st.markdown('####')
        region_chart(region_count, year)

    with col[2]:
        st.markdown(f'#### {year}년 지역별 학생 수 대비 사고 건수')
        create_map(mapdf, '지역', '사고건수/학생수')
        
    st.markdown('####')
    st.markdown('#### 지역별 세부 현황 분석')

    tab_titles = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
    tabs = st.tabs(tab_titles)
        
    # 처리할 지역 목록
    regions = yeardf['지역'].unique()
    region_results = {}
    for region in regions:
        region_df = yeardf[yeardf['지역'] == region]
        processed_data = count_to(region_df['교육청'])
        processed_data['교육청'] = processed_data['교육청'].str.replace('교육지원청', '', regex=False)
        region_results[region] = processed_data

    for tab, title in zip(tabs, tab_titles):
        with tab:
            col = st.columns((3, 2), gap='medium')
            with col[0]:
                create_chart(region_results[title], '교육청')
            with col[1]:
                region_detail_count = df[df['지역'] == title].groupby(['연도', '교육청']).agg(총사고수=('사고발생일', 'count')).reset_index()
                region_detail_count['교육청'] = pd.Categorical(region_detail_count['교육청'])
                region_detail_count['교육청'] = region_detail_count['교육청'].str.replace('교육지원청', '', regex=False)
                region_detail_count = region_detail_count.sort_values(['연도', '교육청']).reset_index(drop=True)
                region_detail_count['전년대비증감률'] = region_detail_count.groupby('교육청')['총사고수'].pct_change().fillna(0) * 100
                region_chart_detail(region_detail_count, year)


    
with tab2:
    geo_order2019 = geodf2019['지역'].tolist()
    region_count['지역'] = pd.Categorical(region_count['지역'], categories=geo_order2019, ordered=True)
    region_count = region_count.sort_values('지역').reset_index(drop=True)
    display_year_tab(2019, df_2019, CTPRVN_2019)

with tab3:
    geo_order2020 = geodf2020['지역'].tolist()
    region_count['지역'] = pd.Categorical(region_count['지역'], categories=geo_order2020, ordered=True)
    region_count = region_count.sort_values('지역').reset_index(drop=True)
    display_year_tab(2020, df_2020, CTPRVN_2020)
    
with tab4:
    geo_order2021 = geodf2021['지역'].tolist()
    region_count['지역'] = pd.Categorical(region_count['지역'], categories=geo_order2021, ordered=True)
    region_count = region_count.sort_values('지역').reset_index(drop=True)
    display_year_tab(2021, df_2021, CTPRVN_2021)
    
with tab5:
    geo_order2022 = geodf2022['지역'].tolist()
    region_count['지역'] = pd.Categorical(region_count['지역'], categories=geo_order2022, ordered=True)
    region_count = region_count.sort_values('지역').reset_index(drop=True)
    display_year_tab(2022, df_2022, CTPRVN_2022)

with tab6:
    geo_order2023 = geodf2023['지역'].tolist()
    region_count['지역'] = pd.Categorical(region_count['지역'], categories=geo_order2023, ordered=True)
    region_count = region_count.sort_values('지역').reset_index(drop=True)
    display_year_tab(2023, df_2023, CTPRVN_2023)

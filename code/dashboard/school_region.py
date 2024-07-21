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
import folium
import json
from function_하윤 import *  # function.py 파일에서 모든 함수 불러오기 

# geojson파일 불러오기
file_path = '../../data/지도 시각화 데이터\TL_SCCO_CTPRVN.json'
geojson = gpd.read_file(file_path)
geojson = geojson.replace('강원도','강원특별자치도') # 강원도 표기 변경
geojson['지역'] = geojson['CTP_KOR_NM'].apply(extract_region) # 학교 안전사고 데이터와 지역 표기 형식 맞추기(충청남도->충북)
geojson_loads = json.loads(geojson.to_json()) # geojson 데이터프레임을 json 형식으로


# 지도 시각화 함수
def create_map(df, location_column, parameter_column):

    fig = px.choropleth_mapbox(
    df,
    geojson=geojson,
    locations=location_column,
    featureidkey="properties." + location_column,
    color=parameter_column,
    color_continuous_scale="OrRd",
    mapbox_style="white-bg",
    zoom=6,
    center={"lat": 36.5, "lon": 127.5},
    opacity=0.5,
    labels={parameter_column: parameter_column}
    )
    
    fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    font=dict({'family':'KoPubWorld돋움체 Medium','color':'black'}), 
    hoverlabel=dict(font_size=15, font_family="KoPubWorld돋움체 Medium"),
    yaxis=dict(tickformat=',')
    )
    
    return fig

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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["5개년 전체","2019년", "2020년", "2021년", "2022년","2023년"])

    with tab1:
        col = st.columns((4.5, 1.5), gap='medium')
        with col[0]:
            st.markdown('#### 지역별 사고 건수 ')
            st.write('호버 수정 필요!!!')
            geoDF_1 = pd.concat([geodf2019, geodf2020, geodf2021, geodf2022, geodf2023],axis=0)

            def create_year_chart(df):
                palette = ["#231942", "#5e548e", "#9f86c0", "#be95c4", "#e0b1cb"]
                customdata_list = []
                for year in df['연도'].unique():
                    customdata_list.append(df[df['연도'] == year]['연도'].tolist())
                # 그래프 생성
                fig = px.bar(df, x='지역', y='건수', color='연도', 
                             labels={'지역': '지역', '건수': '건수', '연도': '연도'},
                             color_discrete_sequence=palette)

                # 레이아웃 설정
                fig.update_layout(font=dict(family='KoPubWorld돋움체_Pro', color='black'),
                                  hoverlabel=dict(font_size=15, font_family='KoPubWorld돋움체_Pro'),
                                  paper_bgcolor='white', plot_bgcolor='white', 
                                  xaxis_tickangle=-45, yaxis=dict(tickformat=',',  title='사고 건수'))

                # hover 설정
                fig.update_traces(
                    hovertemplate='<b>%{x}</b><br>%{customdata[0]}<br>%{y}건<br><extra></extra>',
                    customdata=customdata_list)
                
                return st.plotly_chart(fig)

            create_year_chart(geoDF_1)


            st.markdown('##')
            
            # 지역별 heatmap 생성
            CTPRVN_2019['2019'] = CTPRVN_2019['사고건수/학생수']
            CTPRVN_2020['2020'] = CTPRVN_2020['사고건수/학생수']
            CTPRVN_2021['2021'] = CTPRVN_2021['사고건수/학생수']
            CTPRVN_2022['2022'] = CTPRVN_2022['사고건수/학생수']
            CTPRVN_2023['2023'] = CTPRVN_2023['사고건수/학생수']
            ### 이 부분 코드 수정하기...!!!
            CTPRVN_total = pd.merge(CTPRVN_2019[['지역', '2019']], CTPRVN_2020[['지역', '2020']], on='지역', how='outer')
            CTPRVN_total = pd.merge(CTPRVN_total, CTPRVN_2021[['지역', '2021']], on='지역', how='outer')
            CTPRVN_total = pd.merge(CTPRVN_total, CTPRVN_2022[['지역', '2022']], on='지역', how='outer')
            CTPRVN_total = pd.merge(CTPRVN_total, CTPRVN_2023[['지역', '2023']], on='지역', how='outer')
            CTPRVN_total = CTPRVN_total.set_index('지역')

            CTPRVN_total = CTPRVN_total.sort_values(by='지역', ascending=False)

            colorscale = [[0, '#F7FBFC'], [0.2, '#E6F3F9'], [0.4, '#D6E6F2'], [0.6, '#B9D7EA'], [0.8, '#A2C5E2'], [1, '#769FCD']]
            fig = go.Figure(data=go.Heatmap(
                 z=CTPRVN_total.values, x=CTPRVN_total.columns, y=CTPRVN_total.index[::-1],
                 colorscale=colorscale, colorbar=dict(title='사고 건수')))
            fig.update_layout(xaxis_title='연도', yaxis_title='지역',
                              font=dict(family="KoPubWorld돋움체_Pro", size=12))
            
            st.markdown('#### 연도별 지역별 평균 사고 발생 현황 ') 
            st.plotly_chart(fig)

        
        with col[1]:
            st.markdown('####')
            st.dataframe(count_to(df['지역'])[['지역', '건수']], hide_index=True)


    with tab2:
        col = st.columns((4.5, 1.5), gap='medium')
        with col[0]:
            st.markdown('#### 2019년 지역별 사고 건수 ')
            create_chart(geodf2019, '지역')
        
        with col[1]:
            st.markdown('####')
            st.dataframe(count_to(df_2019['지역'])[['지역', '건수']], hide_index=True)
        
        st.markdown('##')

        st.markdown('#### 지역별 사고건수/학생수')
        acc_spot_oneyear_fig = create_map(CTPRVN_2019, '지역', '사고건수/학생수')
        st.plotly_chart(acc_spot_oneyear_fig, theme="streamlit", use_container_width=True)
    

    with tab3:
        col = st.columns((0.5, 4, 1.5), gap='medium')
        with col[0]:
            # 연도 드롭다운
            years = geoDF_1['연도'].unique()
            selected_year = st.selectbox('연도 선택:', years)

        with col[1]:
            if selected_year == '2019':
                acc_spot_oneyear_fig = create_map(CTPRVN_2019, '지역', '사고건수/학생수')
                st.plotly_chart(acc_spot_oneyear_fig, theme="streamlit", use_container_width=True)
        
        with col[2]:
            if selected_year == '2019':
                st.dataframe(count_to(df_2019['지역'])[['지역', '건수']], hide_index=True)
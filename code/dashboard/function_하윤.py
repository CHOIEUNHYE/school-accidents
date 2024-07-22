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


# chart 생성
def count_to(df):
    series_copy = df.copy()
    series_copy.dropna(inplace=True)
    first_list = series_copy.tolist()

    words_to_split = [word for word in first_list if ',' in str(word)]
    for word in words_to_split:
        first_list.remove(word)
        first_list.extend(word.split(','))

    unique_words = list(set(first_list))
    counts = [first_list.count(word) for word in unique_words]

    count_df = pd.DataFrame({df.name: unique_words, '건수': counts})
    count_df = count_df.sort_values('건수', ascending=False).reset_index(drop=True)

    count_df.reset_index(drop=True, inplace=True)
    per = []

    for i in range(0, len(count_df)):
        per.append(round(count_df['건수'].loc[i] / count_df['건수'].sum() * 100, 2))
    count_df['퍼센트(%)'] = per

    count_df.sort_values(by='퍼센트(%)', ascending=False, inplace=True)
    count_df.reset_index(drop = True, inplace=True)

    return count_df



# bar chart 생성
def create_chart(dfs, theme):
    # 색상 팔레트
    palette = ["#5c7dd2","#92b8ff","#aeceff","#c7e4ff",'#c3b7eb', '#9590e6', '#837ed5']

    # 그래프 생성
    fig = px.bar(dfs, 
                 x=theme, 
                 y='퍼센트(%)', 
                 color=theme,  # theme을 색상으로 사용
                 orientation='v',  # 세로 막대 그래프 설정
                 text='퍼센트(%)',
                 color_discrete_sequence=palette,  # 사용자 지정 색상 팔레트 사용
                 custom_data=['건수', '퍼센트(%)'])

    # 레이아웃 설정
    fig.update_layout(
                font=dict({'family':'KoPubWorld돋움체_Pro',
                        'color':'black'}), #전체 폰트 설정(로컬 폰트 사용 가능)
                hoverlabel=dict(        #호버 박스 폰트 설정
                    font_size=15,
                    font_family="KoPubWorld돋움체_Pro"
                ),
                paper_bgcolor='white',  # 전체 배경색
                plot_bgcolor='white',    # 플롯 배경색
                )

    # 텍스트 설정
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside', textfont_size=12)

    # hover 시 정보 설정
    fig.update_traces(
        hovertemplate='<b><br>%{x}</b></br>%{customdata[1]}</br>건수: %{customdata[0]} 명<br><extra></extra>'
    )

    return st.plotly_chart(fig)



# pie chart 생성
def create_pie_chart(dfs, theme):
    palette = ["#5c7dd2","#92b8ff","#aeceff","#c7e4ff",'#c3b7eb', '#9590e6', '#837ed5']

    # 원 그래프 생성
    fig = px.pie(dfs, 
                 names=theme, 
                 values='퍼센트(%)', 
                 color=theme,  # theme을 색상으로 사용
                 color_discrete_sequence=palette,  # 사용자 지정 색상 팔레트 사용
                 custom_data=['건수', '퍼센트(%)'])

    # 레이아웃 설정
    fig.update_layout(
                font=dict({'family':'KoPubWorld돋움체_Pro',
                        'color':'black'}), # 전체 폰트 설정(로컬 폰트 사용 가능)
                hoverlabel=dict(        # 호버 박스 폰트 설정
                    font_size=15,
                    font_family="KoPubWorld돋움체_Pro"
                ),
                paper_bgcolor='white',  # 전체 배경색
                plot_bgcolor='white',   # 플롯 배경색
                )

    # 텍스트 설정
    fig.update_traces(textinfo='percent+label', textfont_size=12)

    # hover 시 정보 설정
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>퍼센트: %{percent:.1%}<br>건수: %{customdata[0]} 명<br><extra></extra>'
    )
    
    return st.plotly_chart(fig)


# 지역 표기 형식 변경 함수
def extract_region(name):
    if name in ['충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도']:
        return name[:1] + name[2]
    else:
        return name[:2]
    


# 학교별 데이터 전처리 함수 - 시도별
def schooldf1(inputdf):
    df = inputdf.parse('요약정보', skiprows=8)
    df.rename(columns={'행 레이블': '지역', '합계 : 학생수_총계_계':'학생수'}, inplace=True)
    df = df[df['지역'] != '총합계']
    return df


# 학교별 데이터 전처리 함수 - 교육청별
def schooldf2(inputdf):
    df = inputdf.parse('요약정보', skiprows=8)
    df.rename(columns={'행 레이블': '교육청', '합계 : 학생수_총계_계':'학생수'}, inplace=True)
    df = df[df['교육청'] != '총합계']
    return df

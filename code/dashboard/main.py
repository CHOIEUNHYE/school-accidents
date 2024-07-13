# 학교 안전사고 공모전 main 대시보드 파일

#######################
# 라이브러리 임포트
# pip install streamlit
# pip install streamlit-option-menu
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu
import pandas as pd
import polars as pl
import plotly.express as px
from function import *  # function.py 파일에서 모든 함수 불러오기 
import school_accident_details, school_level, school_year, school_region # 각 페이지 구성 py 파일 가져오기


#######################
# 페이지 설정
st.set_page_config(
    page_title="학교 안전사고 현황",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded")


# 글씨체 변경 시도 ㅜㅜ 안 됨
streamlit_style = """ 
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Nanum Gothic', sans-serif;
        }
        </style>
        """
st.markdown(streamlit_style, unsafe_allow_html=True)



#######################
# 데이터 불러오기
df = pd.read_csv('dashboard_data/학교안전사고데이터_5개년통합.csv')
df['사고발생일'] = pd.to_datetime(df['사고발생일'])
df['연도'] = df['사고발생일'].map(lambda x : x.year)


#######################
# 사이드바
with st.sidebar:
    choice = option_menu('학교 안전사고 현황', ["연도별", "지역별", "학교급별","사고내용분석"],
                         icons=['house', 'kanban', 'bi bi-robot','bi bi-robot'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#08c7b4"},
    }
    )


#######################
# 대시보드


if choice == "연도별":
    school_year.run_year(df)

elif choice == "지역별":
    school_region.run_region(df)

elif choice == "학교급별":
    school_level.run_level(df)

elif choice == "사고내용분석":
    school_accident_details.run_details(df)
 


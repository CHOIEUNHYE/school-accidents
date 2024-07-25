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
from function_year_region import *  # function_year_region.py 파일에서 모든 함수 불러오기 
from function_school_level import *  # function_school_level.py 파일에서 모든 함수 불러오기 



#######################
# 페이지 설정
st.set_page_config(
    page_title="학교 안전사고 현황",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded")


with open( "component\style\KoPubWorld Dotum.css" ) as css:
    st.write( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


#########################
# sidebar 멀티 페이지 설정

# 각 페이지 py파일 페이지로 지정
school_home = accident_details = st.Page(
    "school_year.py", title="들어가기", icon=":material/home:")

accident_details = st.Page(
    "school_accident_details.py", title="학교안전사고 내용 분석", icon=":material/done_outline:")

school_level = st.Page("school_level.py", title="학교급별 분석", icon=":material/school:")

school_region = st.Page(
    "school_region.py", title="지역별 분석", icon=":material/location_on:")

school_add = st.Page(
    "school_add.py", title="추가 분석", icon=":material/location_on:")

# sidebar 설정
pg = st.navigation(
    {   

        "🏫학교안전사고 분석 대시보드": [school_home,school_region,school_level,accident_details,school_add]
    }
)

pg.run()

 


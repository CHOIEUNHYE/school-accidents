# 학교 안전사고 공모전 main 대시보드 파일

#######################
# 라이브러리 임포트
# pip install streamlit
# pip install streamlit-option-menu
import streamlit as st
import altair as alt
import pandas as pd
import polars as pl
import plotly.express as px
import os 


#######################
# 페이지 설정
st.set_page_config(
    page_title="학교 안전사고 현황",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded")


# 현재 파일의 디렉토리를 기준으로 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
style_dir = os.path.join(current_dir, "component/style")

# style 디렉토리 하위 파일 목록 출력
if os.path.exists(style_dir):
    file_list = os.listdir(style_dir)
    if file_list:
        st.write("Style 디렉토리 하위의 파일 목록:")
        for file_name in file_list:
            st.write(file_name)
    else:
        st.write("Style 디렉토리에 파일이 없습니다.")
else:
    st.error(f"Style 디렉토리를 찾을 수 없습니다: {style_dir}")

with open( css_file_path ) as css:
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
    "school_add.py", title="추가 분석", icon=":material/bar_chart:")

# sidebar 설정
pg = st.navigation(
    {   

        "🏫학교안전사고 분석 대시보드": [school_home,school_region,school_level,accident_details,school_add]
    }
)

pg.run()

 


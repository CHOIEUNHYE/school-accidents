## 학교급별 분석 streamlit 파일
import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px
from function import *  # function.py 파일에서 모든 함수 불러오기 

def run_level(df):
    # 데이터 전처리
    df_2019 = df[df['사고발생일'].between('2019-01-01', '2019-12-31')]
    df_2020 = df[df['사고발생일'].between('2020-01-01', '2020-12-31')]
    df_2021 = df[df['사고발생일'].between('2021-01-01', '2021-12-31')]
    df_2022 = df[df['사고발생일'].between('2022-01-01', '2022-12-31')]
    df_2023 = df[df['사고발생일'].between('2023-01-01', '2023-12-31')]

    # 대시보드 구성
    st.title('학교급별 사고 현황')
    st.write("여기에 학교급별 내용을 추가합니다.")
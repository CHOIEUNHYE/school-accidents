# 사고 내용 분석 streamlit 파일
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu
import pandas as pd
import polars as pl
import plotly.express as px
from function import *  # function.py 파일에서 모든 함수 불러오기 

def run_details(df):
    # 데이터 전처리
    df_2019 = df[df['사고발생일'].between('2019-01-01', '2019-12-31')]
    df_2020 = df[df['사고발생일'].between('2020-01-01', '2020-12-31')]
    df_2021 = df[df['사고발생일'].between('2021-01-01', '2021-12-31')]
    df_2022 = df[df['사고발생일'].between('2022-01-01', '2022-12-31')]
    df_2023 = df[df['사고발생일'].between('2023-01-01', '2023-12-31')]

    st.title('사고내용분석')
    st.write("여기에 사고분석 내용을 추가합니다.")

    # 레이아웃 나누기 : 1.5 대 4.5 대 2 화면 비율 나눈 거임!!
    col = st.columns((1.5, 4.5), gap='medium')

    with col[0] :
        # column 1 에 담을 내용
        st.markdown('#### 하루 평균 발생 안전 사고 수 ') ##마크다운 문법으로 작성 가능
        acc_spot_oneday_2023 = df_2023.groupby(['사고장소']).count()[['구분']].reset_index().sort_values('구분',ascending=False)
        acc_spot_oneday_2023['하루평균발생사고수'] = round(acc_spot_oneday_2023['구분']/365,1)
        acc_spot_oneday_2023.columns = ['사고장소','총사고수','하루평균발생사고수']
        
        for i in range(0,5):
            st.metric(label=acc_spot_oneday_2023.iloc[i,0],value=str(acc_spot_oneday_2023.iloc[i,2])+'건')

    with col[1] :
        # column 2 에 담을 내용
        st.subheader('장소별 안전사고 발생 현황')
        acc_spot_2019 = get_grouped_count(df_2019,'사고장소',2019)
        acc_spot_2020 = get_grouped_count(df_2020,'사고장소',2020)
        acc_spot_2021 = get_grouped_count(df_2021,'사고장소',2021)
        acc_spot_2022 = get_grouped_count(df_2022,'사고장소',2022)
        acc_spot_2023 = get_grouped_count(df_2023,'사고장소',2023)
        acc_spot = pd.concat([acc_spot_2019,acc_spot_2020,acc_spot_2021,acc_spot_2022,acc_spot_2023]).reset_index(drop=True)
        col = st.columns((4.5, 2), gap='medium')
        with col[0] : # column 2-1
        
            ## 탭 만들기
            tab1, tab2 = st.tabs(["5개년 안전사고 현황", "연도별 안전사고 발생건수"])
            ## 탭별 차트 그리기
            with tab1:
                st.subheader('5개년 안전사고 발생 추이')
                acc_spot_chart = make_px_chart(acc_spot)
                st.plotly_chart(acc_spot_chart, theme="streamlit", use_container_width=True)
            with tab2:
                st.subheader('연도별 안전사고 발생 건수')
                acc_spot_chart = make_px_chart(acc_spot)
                st.plotly_chart(acc_spot_chart, theme="streamlit", use_container_width=True)

        with col[1] :
            # column 3 에 담을 내용
            acc_spot_year_option = st.selectbox(
            "연도 선택",
            ("2019", "2020", "2021","2022",'2023'))
            st.dataframe(acc_spot[acc_spot['연도']==acc_spot_year_option])



    st.subheader('사고부위 & 사고형태')
    acc_spot_2019

    st.divider() ## 구분선

    col = st.columns([2,3])

    with col[0] :
      # column 1 에 담을 내용
      st.title('here is column1')
      st.subheader(' i am column1  subheader !! ')
    
    with col[1] :
      # column 2 에 담을 내용
      st.title('here is column2')
      st.checkbox('this is checkbox1 in col2 ')
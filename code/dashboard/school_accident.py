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

# st.title("학교 안전사고 현황 대시보드")


#######################
# 데이터 불러오기

df = pd.read_csv('dashboard_data/학교안전사고데이터_5개년통합.csv')

df['사고발생일'] = pd.to_datetime(df['사고발생일'])
df['연도'] = df['사고발생일'].map(lambda x : x.year)

df_2019 = df[df['사고발생일'].between('2019-01-01', '2019-12-31')]
df_2020 = df[df['사고발생일'].between('2020-01-01', '2020-12-31')]
df_2021 = df[df['사고발생일'].between('2021-01-01', '2021-12-31')]
df_2022 = df[df['사고발생일'].between('2022-01-01', '2022-12-31')]
df_2023 = df[df['사고발생일'].between('2023-01-01', '2023-12-31')]
del df ## 메모리 관리를 위해서 지웠는데 df 필요하면 지우지 않고 그냥 사용하기 !!


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
    st.title('연도별 사고 현황 ')
    st.write("여기에 연도별 내용을 추가합니다.")

elif choice == "지역별":
    st.title('지역별 사고 현황')
    # 지역별 관련 코드를 여기에 추가합니다.
    st.write("여기에 지역별 내용을 추가합니다.")

elif choice == "학교급별":
    st.title('학교급별 사고 현황')
    # 학교급별 관련 코드를 여기에 추가합니다.
    st.write("여기에 학교급별 내용을 추가합니다.")

elif choice == "사고내용분석":
    st.title('사고내용분석')
    st.write("여기에 사고분석 내용을 추가합니다.")

    # 레이아웃 나누기 : 1.5 대 4.5 대 2 화면 비율 나눈 거임!!
    col = st.columns((1.5, 4.5), gap='medium')

    with col[0] :
        # column 1 에 담을 내용
        st.markdown('#### 하루 평균 발생 <br>안전 사고 수 ') ##마크다운 문법으로 작성 가능
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






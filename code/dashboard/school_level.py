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

df = pd.read_csv('C:/Users/cabby/Desktop/학교안전사고데이터_5개년통합.csv')
sch_df = df[df['사고자구분'].isin(['일반학생', '특수학교(학급)학생', '체육특기학생'])]
st.dataframe(sch_df)

# 그래프 출력 함수_piechart 
def create_piechart(df, year_col, name_col, value_col, name_order, colors):
    
    # 연도 목록 생성
    years = df[year_col].unique()

    # 그래프 생성
    fig = px.pie(df[df[year_col] == years[0]], 
                 names=name_col, 
                 values=value_col,
                 category_orders={name_col: name_order},
                 color=name_col,
                 color_discrete_map=colors,
                 title=f"{years[0]}년 {name_col}별 {value_col}")

    # 드롭다운 메뉴 생성
    dropdown_buttons = [
        {
            'label': str(year),
            'method': 'update',
            'args': [
                {'values': [df[df[year_col] == year][value_col]],
                 'labels': [df[df[year_col] == year][name_col]]}, 
                {'marker.colors': [colors[label] for label in name_order if label in df[df[year_col] == year][name_col].values],
                 'title': f"{year}년 {name_col}별 {value_col}"}
            ]
        }
        for year in years
    ]
     
    # 레이아웃 설정
    fig.update_layout(
        updatemenus=[{
            'buttons': dropdown_buttons,
            'direction': 'down',
            'showactive': True
        }],
        legend=dict(traceorder='normal')
    )
    
    # 퍼센트 포맷 및 hover 설정
    fig.update_traces(texttemplate='%{percent:.2%}',
                      hovertemplate='<b>%{label}</b><br>사고수: %{value}<br>')

    # 그래프 출력
    fig.show()

# 연도, 학교급 기준으로 groupby
sch_tot_acci = sch_df.groupby(['연도', '학교급']).size().reset_index(name='총 사고수')

# 연도 type str로 변경
sch_tot_acci['연도'] = sch_tot_acci['연도'].astype(str)

# 연도, 학교급 기준으로 정렬
custom_order = ["유치원", "초등학교", "중학교", "고등학교", "특수학교", "기타학교"]
sch_tot_acci['학교급'] = pd.Categorical(sch_tot_acci['학교급'], categories=custom_order, ordered=True)
sch_tot_acci = sch_tot_acci.sort_values(['연도', '학교급']).reset_index(drop=True)

st.write(sch_tot_acci)

# 학교급 순서 지정
sch_order = ["유치원", "초등학교", "중학교", "고등학교", "특수학교", "기타학교"]

# 그래프 색 지정
colors = {
    '유치원': '#a9d6e5',
    '초등학교': '#89c2d9',
    '중학교': '#468faf',
    '고등학교': '#2a6f97',
    '특수학교': '#014f86',
    '기타학교': '#013a63'
}

st.title("학교급별 총 사고 수")

# 그래프 출력 함수 실행
st.write(create_piechart(sch_tot_acci, '연도', '학교급', '총 사고수', sch_order, colors))

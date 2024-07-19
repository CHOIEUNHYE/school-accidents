# 학교급별 분석 streamlit 파일
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu
import pandas as pd
import polars as pl
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from function import *  # function.py 파일에서 모든 함수 불러오기 

def create_piechart(df, year_col, grade_col, count_col, order, colors):
    # 그래프 생성
    fig = px.pie(
        df,
        names=grade_col,
        values=count_col,
        color=grade_col,
        category_orders={grade_col: order},
        color_discrete_map=colors,
        title=f"{df[year_col].iloc[0]}년도 {grade_col}별 사고 비율"
    )
    # 퍼센트 포맷 및 hover 설정
    fig.update_traces(texttemplate='%{percent:.2%}',
                      hovertemplate='<b>%{label}</b><br>사고수: %{value}<br>')
    
    # 범례 위치 조정
    fig.update_layout(
        legend=dict(
            x=0.75,  
            y=0.75,  
            xanchor='left',  
            yanchor='middle'  
        )
    )
    # 그래프 출력
    st.plotly_chart(fig)

def create_chart_gender(df, x, y, color, sch_type):
    # 그래프 색 지정
    colors = {
        '남': '#89c2d9',
        '여': '#ffbf69'
    }

    # 그래프 생성
    fig = px.bar(df, x=x, y=y, color=color, color_discrete_map=colors, 
                 title=f"{sch_type} {color}별 {y}", custom_data=['사고자성별','사고수_비율'])
    
    # y축 형식 설정
    fig.update_layout(yaxis=dict(tickformat=","),
                      hoverlabel=dict(font_size=15),
                      paper_bgcolor='white', 
                      plot_bgcolor='white',
                      width=850,
                      height=450,
                      margin=dict(l=200, b=100, t=100)
                      )

    # hover 설정
    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>%{x}<br>사고수: %{y:,}<br>사고수 비율: %{customdata[1]}%<extra></extra>')

    # 그래프 출력
    st.plotly_chart(fig)
    
def run_level(df):
    # 데이터 전처리
    df_2019 = df[df['사고발생일'].between('2019-01-01', '2019-12-31')]
    df_2020 = df[df['사고발생일'].between('2020-01-01', '2020-12-31')]
    df_2021 = df[df['사고발생일'].between('2021-01-01', '2021-12-31')]
    df_2022 = df[df['사고발생일'].between('2022-01-01', '2022-12-31')]
    df_2023 = df[df['사고발생일'].between('2023-01-01', '2023-12-31')]
    
    # 학교급별 분석시 사용될 데이터프레임
    sch_df = df[df['사고자구분'].isin(['일반학생', '특수학교(학급)학생', '체육특기학생'])]
    
    # 선택 가능한 연도 목록 생성
    years = sch_df['연도'].unique()
    
    # 레이아웃 나누기
    st.set_page_config(layout="wide")
    header = st.container()
    col = st.columns((0.5, 4, 1.5), gap='medium')

    with header:
        st.title('학교급별 사고 현황')
        st.write(' ')
    
    with col[0]:
        # 연도 드롭다운 설정
        selected_year = st.selectbox('연도 선택:', years)
        
    with col[1]:
        # 중앙 열에 탭 추가
        tabs = st.tabs(["유치원", "초등학교", "중학교", "고등학교", "특수학교"])
        for tab, school_level in zip(tabs, ["유치원", "초등학교", "중학교", "고등학교", "특수학교"]):
            with tab:
                # 학년이 하나의 값(유아)으로만 이루어진 유치원 제외
                if school_level != "유치원":
                    
                    # 학교급별 데이터 필터링
                    sch_level = sch_df[(sch_df['학교급'] == school_level) & (sch_df['연도'] == selected_year)]
                    
                    # 초등학교의 경우 '사고자학년' 중 유아 값 제외
                    if school_level == "초등학교":
                        sch_level = sch_level[sch_level['사고자학년'] != '유아']
                        
                    # 중학교의 경우 '사고자학년' 중 4학년, 5학년 값 제외
                    elif school_level == "중학교":
                        sch_level = sch_level[~sch_level['사고자학년'].isin(['4학년', '5학년'])]
                        
                    # 연도, 사고자학년 기준으로 groupby
                    sch_grade = sch_level.groupby(['연도', '사고자학년']).size().reset_index(name='사고수')

                    # 연도 type str로 변경
                    sch_grade['연도'] = sch_grade['연도'].astype(str)

                    # 연도, 사고자학년 기준으로 정렬
                    sch_grade = sch_grade.sort_values(['연도', '사고자학년']).reset_index(drop=True)

                    # 그래프 해석 편의를 위해 컬럼명 변경
                    sch_grade.rename(columns={'사고자학년': f'{school_level}_사고자학년'}, inplace=True)

                    # 학년 순서 및 색 지정
                    if school_level == "초등학교":
                        order = ["1학년", "2학년", "3학년", "4학년", "5학년", "6학년"]
                        colors = {
                            '1학년': '#5c7dd2',
                            '2학년': '#92b8ff',
                            '3학년': '#aeceff',  
                            '4학년': '#c7e4ff',
                            '5학년': '#c3b7eb',
                            '6학년': '#9590e6'
                            }
                    elif school_level == "중학교" or school_level == "고등학교":
                        order = ["1학년", "2학년", "3학년"]
                        colors = {
                            '1학년': '#5c7dd2',
                            '2학년': '#92b8ff',
                            '3학년': '#aeceff'
                            }
                    elif school_level == "특수학교":
                        order = ["유아", "1학년", "2학년", "3학년", "4학년", "5학년", "6학년"]
                        colors = {
                            '유아': '#5c7dd2',
                            '1학년': '#92b8ff',
                            '2학년': '#aeceff',  
                            '3학년': '#c7e4ff',
                            '4학년': '#c3b7eb',
                            '5학년': '#9590e6',
                            '6학년': '#837ed5'
                            }

                    # 그래프 출력 함수 실행
                    create_piechart(sch_grade, '연도', f'{school_level}_사고자학년', '사고수', order, colors)         
                
                # 학교 정렬 순서 지정
                custom_order = ["유치원", "초등학교", "중학교", "고등학교", "특수학교", "기타학교"]
                
                # 사고발생일 중 연도만 추출 후 연도, 학교급, 사고자성별 기준으로 groupby
                sch_gender_acci = sch_df.groupby(['연도', '학교급', '사고자성별']).size().reset_index(name='사고수')

                # 연도, 학교급 기준으로 정렬
                sch_gender_acci['학교급'] = pd.Categorical(sch_gender_acci['학교급'], categories=custom_order, ordered=True)
                sch_gender_acci = sch_gender_acci.sort_values(['학교급', '연도']).reset_index(drop=True)

                # 사고자성별별 사고수 비율 계산
                sch_gender_acci['사고수_비율'] = sch_gender_acci.groupby(['연도', '학교급'])['사고수'].transform(lambda x: (x / x.sum() * 100).round(2))

                # 그래프 출력 함수 실행
                create_chart_gender(sch_gender_acci[sch_gender_acci['학교급'] == school_level], '연도', '사고수', '사고자성별', school_level)

                # 연도, 학교급, 사고시간별 사고수 계산
                sch_acci_time = sch_df.groupby(['학교급', '사고시간']).size().reset_index(name='사고수')

                # 학교급 기준으로 정렬
                sch_acci_time['학교급'] = pd.Categorical(sch_acci_time['학교급'], categories=custom_order, ordered=True)
                sch_acci_time = sch_acci_time.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)

                # 연도, 학교급, 사고장소별 사고수 계산
                sch_acci_place = sch_df.groupby(['학교급', '사고장소']).size().reset_index(name='사고수')

                # 학교급 기준으로 정렬
                sch_acci_place['학교급'] = pd.Categorical(sch_acci_place['학교급'], categories=custom_order, ordered=True)
                sch_acci_place = sch_acci_place.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)

                # 연도, 학교급, 사고부위별 사고수 계산
                sch_acci_part = sch_df.groupby(['학교급', '사고부위']).size().reset_index(name='사고수')

                # 학교급 기준으로 정렬
                sch_acci_part['학교급'] = pd.Categorical(sch_acci_part['학교급'], categories=custom_order, ordered=True)
                sch_acci_part = sch_acci_part.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)

                # 그래프 해석 편의를 위해 괄호로 둘러싸인 부분 제거
                sch_acci_part['사고부위'] = sch_acci_part['사고부위'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()

                # 연도, 학교급, 사고형태별 사고수 계산
                sch_acci_type = sch_df.groupby(['학교급', '사고형태']).size().reset_index(name='사고수')

                # 학교급 기준으로 정렬
                sch_acci_type['학교급'] = pd.Categorical(sch_acci_type['학교급'], categories=custom_order, ordered=True)
                sch_acci_type = sch_acci_type.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)

                # 연도, 학교급, 사고당시활동별 사고수 계산
                sch_acci_act = sch_df.groupby(['학교급', '사고당시활동']).size().reset_index(name='사고수')

                # 학교급 기준으로 정렬
                sch_acci_act['학교급'] = pd.Categorical(sch_acci_act['학교급'], categories=custom_order, ordered=True)
                sch_acci_act = sch_acci_act.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)
                
                # 연도, 학교급, 사고매개물별 사고수 계산
                sch_acci_mdm = sch_df.groupby(['학교급', '사고매개물']).size().reset_index(name='사고수')

                # 학교급 기준으로 정렬
                sch_acci_mdm['학교급'] = pd.Categorical(sch_acci_mdm['학교급'], categories=custom_order, ordered=True)
                sch_acci_mdm = sch_acci_mdm.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)

                # 그래프 해석 편의를 위해 괄호로 둘러싸인 부분 제거
                sch_acci_mdm['사고매개물'] = sch_acci_mdm['사고매개물'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()

                # 서브플롯 생성
                fig = make_subplots(
                    rows=2, cols=3, 
                    subplot_titles=("사고 시간", "사고 장소", "사고 부위", "사고 형태", "사고 당시 활동", "사고 매개물"), 
                    horizontal_spacing=0.15
                    )

                # 사고 시간 그래프 생성
                time_data = sch_acci_time[sch_acci_time['학교급'] == school_level].sort_values('사고수', ascending=False).head(5)
                fig.add_trace(
                    go.Bar(y=time_data['사고시간'], x=time_data['사고수'], name="사고시간", orientation='h', marker=dict(color='#aeceff'),
                           hovertemplate='<b>사고시간</b><br>%{y}<br>사고수: %{x:,}<extra></extra>'),
                    row=1, col=1
                )
                fig.update_yaxes(categoryorder='total ascending', tickfont=dict(size=13), row=1, col=1)

                # 사고 장소 그래프 생성
                place_data = sch_acci_place[sch_acci_place['학교급'] == school_level].sort_values('사고수', ascending=False).head(5)
                fig.add_trace(
                    go.Bar(y=place_data['사고장소'], x=place_data['사고수'], name="사고장소", orientation='h', marker=dict(color='#aeceff'),
                        hovertemplate='<b>사고장소</b><br>%{y}<br>사고수: %{x:,}<extra></extra>'),
                    row=1, col=2
                )
                fig.update_yaxes(categoryorder='total ascending', tickfont=dict(size=13), row=1, col=2)

                # 사고 부위 그래프 생성
                part_data = sch_acci_part[sch_acci_part['학교급'] == school_level].sort_values('사고수', ascending=False).head(5)
                fig.add_trace(
                    go.Bar(y=part_data['사고부위'], x=part_data['사고수'], name="사고부위", orientation='h', marker=dict(color='#aeceff'),
                           hovertemplate='<b>사고부위</b><br>%{y}<br>사고수: %{x:,}<extra></extra>'),
                    row=1, col=3
                )
                fig.update_yaxes(categoryorder='total ascending', tickfont=dict(size=13), row=1, col=3)
                
                # 사고 형태 그래프 생성
                type_data = sch_acci_type[sch_acci_type['학교급'] == school_level].sort_values('사고수', ascending=False).head(5)
                fig.add_trace(
                    go.Bar(y=type_data['사고형태'], x=type_data['사고수'], name="사고형태", orientation='h', marker=dict(color='#aeceff'),
                        hovertemplate='<b>사고형태</b><br>%{y}<br>사고수: %{x:,}<extra></extra>'),
                    row=2, col=1
                )
                fig.update_yaxes(categoryorder='total ascending', tickfont=dict(size=13), row=2, col=1)
                
                # 사고 당시 활동 그래프 생성
                act_data = sch_acci_act[sch_acci_act['학교급'] == school_level].sort_values('사고수', ascending=False).head(5)
                fig.add_trace(
                    go.Bar(y=act_data['사고당시활동'], x=act_data['사고수'], name="사고당시활동", orientation='h', marker=dict(color='#5c7dd2'),
                           hovertemplate='<b>사고당시활동</b><br>%{y}<br>사고수: %{x:,}<extra></extra>'),
                    row=2, col=2
                )
                fig.update_yaxes(categoryorder='total ascending', tickfont=dict(size=13), row=2, col=2)
    
                # 사고 매개물 그래프 생성
                mdm_data = sch_acci_mdm[sch_acci_mdm['학교급'] == school_level].sort_values('사고수', ascending=False).head(5)
                fig.add_trace(
                    go.Bar(y=mdm_data['사고매개물'], x=mdm_data['사고수'], name="사고매개물", orientation='h', marker=dict(color='#9590e6'),
                           hovertemplate='<b>사고매개물</b><br>%{y}<br>사고수: %{x:,}<extra></extra>'),
                    row=2, col=3
                )
                fig.update_yaxes(categoryorder='total ascending', tickfont=dict(size=13), row=2, col=3)

                # 레이아웃 조정
                fig.update_layout(height=800, width=900, 
                                  title_text=f"{school_level}별 (5개년 누적)", 
                                  showlegend=True,
                                  legend=dict(
                                      orientation="h",
                                      yanchor="bottom",
                                      y=1.1,
                                      xanchor="left",
                                      x=0),
                                  margin=dict(t=250, b=50)
                                  )
                
                # 그래프 출력
                st.plotly_chart(fig)

    with col[2]:
        st.markdown('#### 학교급별 총 사고수')
    
        # 선택한 연도에 따라 데이터 필터링
        df_selected_year = sch_df[sch_df['연도'] == selected_year]
    
        # 학교급별 사고수 groupby
        sch_tot_acci = df_selected_year.groupby(['학교급']).size().reset_index(name='총 사고수')
    
        # 학교급 기준으로 정렬
        custom_order = ["유치원", "초등학교", "중학교", "고등학교", "특수학교", "기타학교"]
        sch_tot_acci['학교급'] = pd.Categorical(sch_tot_acci['학교급'], categories=custom_order, ordered=True)
        sch_tot_acci = sch_tot_acci.sort_values(['총 사고수', '학교급'], ascending=[False, True]).reset_index(drop=True)

        max_value = int(sch_tot_acci["총 사고수"].max())
        
        st.dataframe(sch_tot_acci,
                     hide_index=True,
                     width=300,
                     column_config={
                         "학교급": st.column_config.TextColumn(
                             "학교급",
                             ),
                         "총 사고수": st.column_config.ProgressColumn(
                             "총 사고수",
                             format="%d",
                             min_value=0,
                             max_value=max_value,
                             )}
                    )
    
        # 연도, 학교급 기준으로 groupby 후 각 연도와 학교급별 총 사고발생일 수 계산
        sch_aver_acci = sch_df.groupby(['연도', '학교급']).agg(총사고수=('사고발생일', 'count')).reset_index()
        
        # 연도, 학교급 기준으로 정렬
        custom_order = ["유치원", "초등학교", "중학교", "고등학교", "특수학교", "기타학교"]
        sch_aver_acci['학교급'] = pd.Categorical(sch_aver_acci['학교급'], categories=custom_order, ordered=True)
        sch_aver_acci = sch_aver_acci.sort_values(['연도', '학교급']).reset_index(drop=True)

        # 하루 평균 사고 발생 수 계산
        sch_aver_acci['하루평균사고수'] = round(sch_aver_acci['총사고수'] / 365, 2)

        # 전년 대비 증감률 계산
        sch_aver_acci['전년대비증감률'] = sch_aver_acci.groupby('학교급')['하루평균사고수'].pct_change().fillna(0) * 100

        # 선택한 연도에 해당하는 데이터 필터링
        current_data = sch_aver_acci[(sch_aver_acci['연도'] == selected_year)]

        st.markdown("#### 하루평균사고수")
        for index, row in current_data.iterrows():
            school_level = row['학교급']
            average_accidents = row['하루평균사고수']
            change_rate = row['전년대비증감률']
            change_color = 'green' if change_rate > 0 else 'red'
            change_icon = '↑' if change_rate > 0 else '↓'

            st.markdown(f"<h4 style='text-align: center;'>{school_level}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'><strong>{average_accidents}</strong></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; color: {change_color};'>{change_icon} {abs(change_rate):.2f}%</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    # 실제 데이터 파일 경로로 교체
    file_path = 'C:/Users/cabby/Desktop/학교안전사고데이터_5개년통합.csv'
    # 데이터 파일을 읽어오기
    df = pd.read_csv(file_path)
    
    run_level(df)

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

def run_level(df):
    # 데이터 전처리
    df_2019 = df[df['사고발생일'].between('2019-01-01', '2019-12-31')]
    df_2020 = df[df['사고발생일'].between('2020-01-01', '2020-12-31')]
    df_2021 = df[df['사고발생일'].between('2021-01-01', '2021-12-31')]
    df_2022 = df[df['사고발생일'].between('2022-01-01', '2022-12-31')]
    df_2023 = df[df['사고발생일'].between('2023-01-01', '2023-12-31')]
    
    # 학교급별 분석시 사용될 데이터프레임
    sch_df = df[df['사고자구분'].isin(['일반학생', '특수학교(학급)학생', '체육특기학생'])]
    # 연도 type str로 변경
    sch_df['연도'] = sch_df['연도'].astype(str)
    
    # 초등학교 저학년과 고학년으로 구분한 데이터프레임
    sch_df_level_div = sch_df.copy()
    sch_df_level_div['학교급'] = sch_df_level_div.apply(update_school_level, axis=1)
  
    st.markdown('''
    <h1 style="font-family: 'KoPubWorld Dotum', sans-serif; text-align: center;">
        학교안전사고 학교급별 분석
    </h1>
    ''', unsafe_allow_html=True)
    
    st.markdown('######')
    st.write('2019년~2023년 5개년간의 학교급별 안전사고 발생 현황에 대한 정보를 제공합니다. 학교 특성에 따른 안전사고 발생 현황을 상세히 확인할 수 있습니다.')
    st.write('안전사고 중 학생이 당한 사고에 초점을 맞춰 분석 시 사고자구분 값 중 일반학생, 특수학교(학급)학생, 체육특기학생만을 대상으로 하였습니다.')
    st.markdown('######')     
       
    # 전체 레이아웃 설정
    col = st.columns((1, ), gap='medium')
    
    # 탭 정의
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["2019년", "2020년", "2021년", "2022년", "2023년"])
    
    with col[0]:
        # sch_aver_acci 데이터프레임
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
            
        # sch_tot_acci 데이터프레임
        # 연도, 학교급 기준으로 groupby
        sch_tot_acci = sch_df_level_div.groupby(['연도', '학교급']).size().reset_index(name='총 사고수')
        # 연도 type str로 변경
        sch_tot_acci['연도'] = sch_tot_acci['연도'].astype(str)
        # 연도, 학교급 기준으로 정렬
        custom_order = ["유치원", "초등학교_저학년", "초등학교_고학년", "중학교", "고등학교", "특수학교", "기타학교"]
        sch_tot_acci['학교급'] = pd.Categorical(sch_tot_acci['학교급'], categories=custom_order, ordered=True)
        sch_tot_acci = sch_tot_acci.sort_values(['연도', '학교급']).reset_index(drop=True)
        # update_school_level 함수 적용 과정에서 생긴 nan 값(사고자학년 값이 유아인 경우) 처리
        sch_tot_acci = sch_tot_acci.dropna()
    
        # sch_gender_acci 데이터프레임
        # 사고발생일 중 연도만 추출 후 연도, 학교급, 사고자성별 기준으로 groupby
        sch_gender_acci = sch_df.groupby(['연도', '학교급', '사고자성별']).size().reset_index(name='사고수')
        # 기타학교 값 제외
        sch_gender_acci = sch_gender_acci[sch_gender_acci['학교급']!='기타학교']
        # 연도, 학교급 기준으로 정렬
        custom_order = ["유치원", "초등학교", "중학교", "고등학교", "특수학교", "기타학교"]
        sch_gender_acci['학교급'] = pd.Categorical(sch_gender_acci['학교급'], categories=custom_order, ordered=True)
        sch_gender_acci = sch_gender_acci.sort_values(['학교급','연도']).reset_index(drop=True)
        # 사고자성별별 사고수 비율 계산
        sch_gender_acci['사고수 비율'] = sch_gender_acci.groupby(['연도', '학교급'])['사고수'].transform(lambda x: (x / x.sum() * 100).round(2))
    
        # 탭별 그래프 추가 함수  
        def render_tab(year):
            col = st.columns((1, 5), gap='medium')
            with col[0]:
                # sch_aver_acci 그래프 시각화
                sch_aver_acci_chart(sch_aver_acci, year)

            with col[1]:
                # sch_tot_acci 그래프 시각화
                custom_order = ["유치원", "초등학교_저학년", "초등학교_고학년", "중학교", "고등학교", "특수학교", "기타학교"]
                colors = {
                    "유치원": '#5c7dd2', 
                    "초등학교_저학년": '#92b8ff', 
                    "초등학교_고학년": '#aeceff', 
                    "중학교": '#c7e4ff', 
                    "고등학교": '#c3b7eb', 
                    "특수학교": '#9590e6', 
                    "기타학교": '#837ed5'
                    }
                st.plotly_chart(create_piechart(sch_tot_acci, year, '학교급', '총 사고수', custom_order, colors))
                st.divider()
                
                # sch_gender_acci 그래프 시각화
                st.plotly_chart(create_pyramid_chart(sch_gender_acci, year))
                st.divider()
                
        # 각 탭에서의 함수 실행
        with tab1:
            render_tab('2019')
            
        with tab2:
            render_tab('2020')
        with tab3:
            render_tab('2021')
        with tab4:
            render_tab('2022')
        with tab5:
            render_tab('2023')
    
    # 데이터 전처리
    sch_df['사고월'] = sch_df['사고발생일'].apply(lambda x: str(x.month) + '월')
    sch_df['계절'] = sch_df['사고발생일'].apply(get_season)
    temp_df = sch_df.copy()
        
    # 초등 저학년 고학년 나누기
    temp_df.loc[(temp_df['학교급']=='초등학교')&(temp_df['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등학교(저학년)'
    temp_df.loc[(temp_df['학교급']=='초등학교')&(temp_df['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등학교(고학년)'


    # 각 사고월별 총 사고 건수 계산
    total_by_school = temp_df.groupby('사고월')['구분'].count()

    # 각 행에 대해 퍼센트를 계산하여 새로운 컬럼 추가
    level_month = temp_df.groupby(['학교급','사고월']).count()[['구분']].reset_index()
    level_month['퍼센트'] = level_month.apply(lambda row:round((row['구분'] / total_by_school[row['사고월']]) * 100,1), axis=1)
    level_month
    months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
    level_month_pivot = level_month.pivot_table(index='사고월', columns='학교급', values=['퍼센트','구분']).reindex(index=months)
    school_type_categories = ["유치원", "초등학교(저학년)", "초등학교(고학년)", "중학교", "고등학교", "특수학교"]
    palette = ['#5c7dd2','#92b8ff','#aeceff','#c7e4ff','#c3b7eb', '#9590e6', '#837ed5']

    st.plotly_chart(create_stacked_barchart(level_month_pivot, school_type_categories, palette, months))

    # 탭 정의
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["사고 시간", "사고 장소", "사고 부위", "사고 형태", "사고 당시 활동", "사고 매개물"])
    
    with col[0]:
        
        # 학교급 정렬 기준 지정
        custom_order = ["유치원", "초등학교", "중학교", "고등학교", "특수학교"]

        # sch_acci_time 데이터프레임(사고시간 5개년 누적)
        # 분석 편의를 위해 일부 데이터 값 변경
        sch_acci_time = sch_df[sch_df['학교급'] != '기타학교']
        sch_acci_time = sch_acci_time.replace('점심시간', '식사시간')
        sch_acci_time = sch_acci_time.replace('석식시간', '식사시간')
        sch_acci_time = sch_acci_time.replace('휴식시간 및 청소시간', '휴식/청소시간')
        # 연도, 학교급, 사고시간별 사고수 계산
        sch_acci_time = sch_acci_time.groupby(['학교급', '사고시간']).size().reset_index(name='사고수')
        # 학교급 기준으로 정렬
        sch_acci_time['학교급'] = pd.Categorical(sch_acci_time['학교급'], categories=custom_order, ordered=True)
        sch_acci_time = sch_acci_time.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)
        
        # sch_acci_place 데이터프레임(사고장소 5개년 누적)
        # 분석 편의를 위해 일부 데이터 값 변경
        sch_acci_place = sch_df[sch_df['학교급'] != '기타학교']
        sch_acci_place = sch_acci_place.replace('교외활동', '교외')
        # 연도, 학교급, 사고장소별 사고수 계산
        sch_acci_place = sch_acci_place.groupby(['학교급', '사고장소']).size().reset_index(name='사고수')
        # 학교급 기준으로 정렬
        sch_acci_place['학교급'] = pd.Categorical(sch_acci_place['학교급'], categories=custom_order, ordered=True)
        sch_acci_place = sch_acci_place.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)
        
        # sch_acci_part 데이터프레임(사고부위 5개년 누적)
        # 분석 편의를 위해 일부 데이터 값 변경
        sch_acci_part = sch_df[sch_df['학교급'] != '기타학교']
        sch_acci_part['사고부위'] = sch_acci_part['사고부위'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()
        # 연도, 학교급, 사고부위별 사고수 계산
        sch_acci_part = sch_acci_part.groupby(['학교급', '사고부위']).size().reset_index(name='사고수')
        # 학교급 기준으로 정렬
        sch_acci_part['학교급'] = pd.Categorical(sch_acci_part['학교급'], categories=custom_order, ordered=True)
        sch_acci_part = sch_acci_part.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)
        
        # sch_acci_type 데이터프레임(사고형태 5개년 누적)
        # 분석 편의를 위해 일부 데이터 값 변경
        sch_acci_type = sch_df[sch_df['학교급'] != '기타학교']
        sch_acci_type = sch_acci_type.replace('낙상-미끄러짐', '낙상')
        sch_acci_type = sch_acci_type.replace('낙상-넘어짐', '낙상')
        sch_acci_type = sch_acci_type.replace('낙상-떨어짐', '낙상')
        sch_acci_type = sch_acci_type.replace('염좌·삐임 등 신체 충격', '염좌/삐임/신체 충격')
        # 연도, 학교급, 사고형태별 사고수 계산
        sch_acci_type = sch_acci_type.groupby(['학교급', '사고형태']).size().reset_index(name='사고수')
        # 학교급 기준으로 정렬
        sch_acci_type['학교급'] = pd.Categorical(sch_acci_type['학교급'], categories=custom_order, ordered=True)
        sch_acci_type = sch_acci_type.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)
        
        # sch_acci_act 데이터프레임(사고당시활동 5개년 누적)
        # 연도, 학교급, 사고당시활동별 사고수 계산
        sch_acci_act = sch_df[sch_df['학교급'] != '기타학교']
        sch_acci_act = sch_df.groupby(['연도', '학교급', '사고당시활동']).size().reset_index(name='사고수')
        # 연도, 학교급 기준으로 정렬
        sch_acci_act['학교급'] = pd.Categorical(sch_acci_act['학교급'], categories=custom_order, ordered=True)
        sch_acci_act = sch_acci_act.sort_values(['연도', '학교급']).reset_index(drop=True)
        
        # sch_acci_mdm 데이터프레임(사고매개물 5개년 누적)
        # 분석 편의를 위해 일부 데이터 값 변경
        sch_acci_mdm = sch_df[sch_df['학교급'] != '기타학교']
        sch_acci_mdm['사고매개물'] = sch_acci_mdm['사고매개물'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()
        # 연도, 학교급, 사고매개물별 사고수 계산
        sch_acci_mdm = sch_acci_mdm.groupby(['연도', '학교급', '사고매개물']).size().reset_index(name='사고수')
        # 연도, 학교급 기준으로 정렬
        sch_acci_mdm['학교급'] = pd.Categorical(sch_acci_mdm['학교급'], categories=custom_order, ordered=True)
        sch_acci_mdm = sch_acci_mdm.sort_values(['연도', '학교급']).reset_index(drop=True)
        
        # 사고 시간 탭
        with tab1:
            st.plotly_chart(create_barchart(sch_acci_time, '사고시간', '사고수', '학교급별 사고 시간'))
        # 사고 장소 탭
        with tab2:
            st.plotly_chart(create_barchart(sch_acci_place, '사고장소', '사고수', '학교급별 사고 장소'))
        # 사고 부위 탭
        with tab3:
            st.plotly_chart(create_barchart(sch_acci_part, '사고부위', '사고수', '학교급별 사고 부위'))
        # 사고 형태 탭
        with tab4:
            st.plotly_chart(create_barchart(sch_acci_type, '사고형태', '사고수', '학교급별 사고 형태'))
        # 사고 당시 활동 탭
        with tab5:
            st.plotly_chart(create_barchart(sch_acci_act, '사고당시활동', '사고수', '학교급별 사고 당시 활동'))
        # 사고 매개물 탭
        with tab6:
            st.plotly_chart(create_barchart(sch_acci_mdm, '사고매개물', '사고수', '학교급별 사고 매개물'))                
        
''' 

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
'''
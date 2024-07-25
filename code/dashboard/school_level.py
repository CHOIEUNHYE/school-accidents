# 학교급별 분석 streamlit 파일
import streamlit as st
import pandas as pd
import polars as pl
from function_school_level import *  # function_school_level.py 파일에서 모든 함수 불러오기 

# 폰트 설정
with open( "component\style\KoPubWorld Dotum.css" ) as css:
    st.write( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

with open( "component\style\style.css" ) as css:
    st.write( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

#######################
#데이터 불러오기

df = pl.read_csv('../../../school-accidents/code/dashboard/component/data/학교안전사고데이터통합/학교안전사고데이터_5개년통합_월계절추가.csv')
df = df.to_pandas()
df['사고발생일'] = pd.to_datetime(df['사고발생일'])
df['연도'] = df['사고발생일'].map(lambda x : x.year)

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
    sch_tot_acci = sch_df.groupby(['연도', '학교급']).size().reset_index(name='총 사고수')
    # 연도, 학교급 기준으로 정렬
    custom_order = ["유치원", "초등학교", "중학교", "고등학교", "특수학교", "기타학교"]
    sch_tot_acci['학교급'] = pd.Categorical(sch_tot_acci['학교급'], categories=custom_order, ordered=True)
    sch_tot_acci = sch_tot_acci.sort_values(['연도', '학교급']).reset_index(drop=True)
        
    # sch_tot_acci2 데이터프레임
    sch_tot_acci2 = sch_df.copy()
    # 초등학교 저학년/고학년 구분
    sch_tot_acci2.loc[(sch_tot_acci2['학교급']=='초등학교')&(sch_tot_acci2['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등학교(저학년)'
    sch_tot_acci2.loc[(sch_tot_acci2['학교급']=='초등학교')&(sch_tot_acci2['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등학교(고학년)'
    # 연도, 학교급 기준으로 groupby
    sch_tot_acci2 = sch_tot_acci2.groupby(['연도', '학교급']).size().reset_index(name='총 사고수')
    # 연도, 학교급 기준으로 정렬
    custom_order = ["유치원", "초등학교(저학년)", "초등학교(고학년)", "중학교", "고등학교", "특수학교", "기타학교"]
    sch_tot_acci2['학교급'] = pd.Categorical(sch_tot_acci2['학교급'], categories=custom_order, ordered=True)
    sch_tot_acci2 = sch_tot_acci2.sort_values(['연도', '학교급']).reset_index(drop=True)
    # update_school_level 함수 적용 과정에서 생긴 nan 값(사고자학년 값이 유아인 경우) 처리
    sch_tot_acci2 = sch_tot_acci2.dropna()

    # sch_gender_acci 데이터프레임
    # 기타학교 값 제외
    sch_gender_acci = sch_df[sch_df['학교급'] != '기타학교']
    # 초등학교 저학년/고학년 구분
    sch_gender_acci.loc[(sch_gender_acci['학교급']=='초등학교')&(sch_gender_acci['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등학교(저학년)'
    sch_gender_acci.loc[(sch_gender_acci['학교급']=='초등학교')&(sch_gender_acci['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등학교(고학년)'
    # 연도, 학교급, 사고자성별 기준으로 groupby
    sch_gender_acci = sch_gender_acci.groupby(['연도', '학교급', '사고자성별']).size().reset_index(name='사고수')
    # 연도, 학교급 기준으로 정렬
    custom_order = ["유치원", "초등학교(저학년)", "초등학교(고학년)", "중학교", "고등학교", "특수학교", "기타학교"]
    sch_gender_acci['학교급'] = pd.Categorical(sch_gender_acci['학교급'], categories=custom_order, ordered=True)
    sch_gender_acci = sch_gender_acci.sort_values(['학교급','연도']).reset_index(drop=True)
    # 사고자성별별 사고수 비율 계산
    sch_gender_acci['사고수 비율'] = sch_gender_acci.groupby(['연도', '학교급'])['사고수'].transform(lambda x: (x / x.sum() * 100).round(2))
    # 초등학교 저학년/고학년 구분 과정에서 생긴 nan 값(사고자학년 값이 유아인 경우) 처리
    sch_gender_acci = sch_gender_acci.dropna()

    # sch_grade_acci 데이터프레임
    # '학교급'의 '유치원', '기타학교' 값 '사고자학년'의 'nan' 값 제외
    sch_grade_acci = sch_df[
        (sch_df['학교급'] != '기타학교') &
        (sch_df['학교급'] != '유치원') &
        (sch_df['사고자학년'] != 'nan')
        ]
    # 연도, 학교급, 사고자학년 기준으로 groupby
    sch_grade_acci = sch_grade_acci.groupby(['연도', '학교급', '사고자학년']).size().reset_index(name='사고수')
    # '초등학교'의 '사고자학년'에서 '유아' 값을 제외
    sch_grade_acci = sch_grade_acci[~((sch_grade_acci['학교급'] == '초등학교') & 
                                        (sch_grade_acci['사고자학년'] == '유아'))]
    # '중학교'의 '사고자학년'에서 '4학년'과 '5학년' 값을 제외
    sch_grade_acci = sch_grade_acci[~((sch_grade_acci['학교급'] == '중학교') & 
                                        ((sch_grade_acci['사고자학년'] == '4학년') | 
                                        (sch_grade_acci['사고자학년'] == '5학년')))]
    # 연도, 학교급 기준으로 정렬
    custom_order = ["유치원", "초등학교", "중학교", "고등학교", "특수학교"]
    sch_grade_acci['학교급'] = pd.Categorical(sch_grade_acci['학교급'], categories=custom_order, ordered=True)
    sch_grade_acci = sch_grade_acci.sort_values(['학교급','연도']).reset_index(drop=True)

    # 탭별 그래프 추가 함수  
    def render_tab(year):
        col = st.columns((1, 5), gap='medium')
        with col[0]:
            # sch_aver_acci 그래프 시각화
            sch_aver_acci_chart(sch_aver_acci, year)

        with col[1]:
            col = st.columns((2.5, 2.5), gap='medium')
            with col[0]:
                # sch_tot_acci 그래프 시각화
                st.markdown('######')
                st.markdown(f'''
                            <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
                            {year}년 학교급별 총 사고 수
                            </h4>
                            ''', unsafe_allow_html=True)
                custom_order = ["기타학교", "특수학교", "고등학교", "중학교", "초등학교", "유치원"]
                st.plotly_chart(create_h_barchart(sch_tot_acci, year, "총 사고수", "학교급", custom_order))
                
            with col[1]:
                # sch_tot_acci2 그래프 시각화
                st.markdown('###')
                custom_order = ["유치원", "초등학교(저학년)", "초등학교(고학년)", "중학교", "고등학교", "특수학교", "기타학교"]
                colors = {
                    "유치원": '#5c7dd2', 
                    "초등학교(저학년)": '#92b8ff', 
                    "초등학교(고학년)": '#aeceff', 
                    "중학교": '#c7e4ff', 
                    "고등학교": '#c3b7eb', 
                    "특수학교": '#9590e6', 
                    "기타학교": '#837ed5'
                    }
                st.plotly_chart(create_piechart(sch_tot_acci2, year, '학교급', '총 사고수', custom_order, colors))
            
            st.markdown('######')
            st.markdown('학교급별 총 사고 수에 대한 정보를 각각의 연도마다 제공합니다. 특정 연도에 어느 학교급에서 사고가 가장 많이 발생했는지 양상을 파악할 수 있습니다.', unsafe_allow_html=True)
            st.markdown('초등학교의 경우, 저학년과 고학년의 특성이 서로 다르다고 보아 이를 구분하여 추가 분석을 실시하였습니다.', unsafe_allow_html=True)
            st.divider()
            
            col = st.columns((3, 2), gap='medium')
            with col[0]:
                # sch_gender_acci 그래프 시각화
                st.markdown('######')
                st.markdown(f'''
                            <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
                            {year}년 학교급별 사고자 성별
                            </h4>
                            ''', unsafe_allow_html=True)
                st.plotly_chart(create_pyramid_chart(sch_gender_acci, year, '사고수', '학교급'))
            
            with col[1]:
                st.markdown('######')
                st.markdown(f'''
                            <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
                            {year}년 학교급별 사고자 학년
                            </h4>
                            ''', unsafe_allow_html=True)
                # sch_grade_acci 그래프 시각화
                # 탭 정의
                st.markdown('######')
                tab1, tab2, tab3, tab4 = st.tabs(["초등", "중등", "고등", "특수"])
                # 각 탭에서의 함수 실행
                with tab1:
                    # 사고자학년 순서 지정
                    es_order = ["1학년", "2학년", "3학년", "4학년", "5학년", "6학년"]
                    # 그래프 색 지정
                    es_colors = {
                        '1학년': '#92b8ff',
                        '2학년': '#aeceff',
                        '3학년': '#c7e4ff',
                        '4학년': '#c3b7eb',
                        '5학년': '#9590e6',
                        '6학년': '#837ed5'
                        }
                    st.plotly_chart(create_donut_chart(sch_grade_acci, year, '초등학교', '사고자학년', '사고수', es_order, es_colors))
                with tab2:
                    # 사고자학년 순서 지정
                    ms_order = ["1학년", "2학년", "3학년"]
                    # 그래프 색 지정
                    ms_colors = {
                        '1학년': '#92b8ff',
                        '2학년': '#aeceff',
                        '3학년': '#c7e4ff'
                        }
                    st.plotly_chart(create_donut_chart(sch_grade_acci, year, '중학교', '사고자학년', '사고수', ms_order, ms_colors))
                with tab3:
                    # 사고자학년 순서 지정
                    hs_order = ["1학년", "2학년", "3학년"]
                    # 그래프 색 지정
                    hs_colors = {
                        '1학년': '#92b8ff',
                        '2학년': '#aeceff',
                        '3학년': '#c7e4ff'
                        }
                    st.plotly_chart(create_donut_chart(sch_grade_acci, year, '고등학교', '사고자학년', '사고수', hs_order, hs_colors))
                with tab4:
                    # 사고자학년 순서 지정
                    ss_order = ["유아", "1학년", "2학년", "3학년", "4학년", "5학년", "6학년"]
                    # 그래프 색 지정
                    ss_colors = {
                        '유아': '#5c7dd2',
                        '1학년': '#92b8ff',
                        '2학년': '#aeceff',
                        '3학년': '#c7e4ff',
                        '4학년': '#c3b7eb',
                        '5학년': '#9590e6',
                        '6학년': '#837ed5'
                        }
                    st.plotly_chart(create_donut_chart(sch_grade_acci, year, '특수학교', '사고자학년', '사고수', ss_order, ss_colors))
        
        st.markdown('######')
        st.markdown('좌측 시각화는 학교급별 사고자 성별에 따른 사고 수에 대한 정보를 각각의 연도마다 제공합니다. 특정 연도에서의 학교급별 총 사고자의 성별 비율을 파악할 수 있습니다.', unsafe_allow_html=True)
        st.markdown('분석을 진행하면서 학교급 중 기타학교는 학교의 특성을 파악하기 어렵다고 보아 분석 대상에서 제외하였습니다. 초등학교의 경우에는 저학년과 고학년의 특성이 서로 다르다고 보아 이를 구분해 분석하였습니다.', unsafe_allow_html=True)
        st.markdown('우측 시각화는 학교급별 사고자 학년에 따른 사고 수에 대한 정보를 각각의 연도마다 제공합니다. 특정 연도에서의 학교급별 총 사고자의 학년 비율을 파악할 수 있습니다.', unsafe_allow_html=True)
        st.markdown('분석을 진행하면서 학교급 중 유치원은 학년이 따로 구분되어 있지 않았고, 기타학교는 학교의 특성을 파악하기 어렵다고 판단하여 모두 분석 대상에서 제외하였습니다. 일반적인 학년 체계에 따라 분석을 진행하고자 초등학교에서의 유아 값과 중학교에서의 4, 5학년 값 또한 제외하고 분석하였습니다.', unsafe_allow_html=True)
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

# sch_month_acci 데이터프레임
sch_month_acci = sch_df.copy()
# 초등학교 저학년/고학년 구분
sch_month_acci.loc[(sch_month_acci['학교급']=='초등학교')&(sch_month_acci['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등학교(저학년)'
sch_month_acci.loc[(sch_month_acci['학교급']=='초등학교')&(sch_month_acci['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등학교(고학년)'
# 각 사고월별 총 사고 건수 계산
sch_month_tot_acci = sch_month_acci.groupby('사고월')['구분'].count()
# 각 행에 대해 퍼센트를 계산하여 새로운 컬럼 추가
month_level = sch_month_acci.groupby(['학교급','사고월']).count()[['구분']].reset_index()
month_level['퍼센트'] = month_level.apply(lambda row:round((row['구분'] / sch_month_tot_acci[row['사고월']]) * 100, 2), axis=1)
months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
month_level_pivot = month_level.pivot_table(index='사고월', columns='학교급', values=['퍼센트','구분']).reindex(index=months)
sch_type_cat = ["유치원", "초등학교(저학년)", "초등학교(고학년)", "중학교", "고등학교", "특수학교", "기타학교"]
colors = ['#5c7dd2','#92b8ff','#aeceff','#c7e4ff','#c3b7eb', '#9590e6', '#837ed5', '#5843a9']

col = st.columns((0.5, 5, 0.5), gap='medium')
with col[1]:
    # sch_month_acci 그래프 시각화
    st.markdown('######')
    st.markdown(f'''
                <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0; text-align: center;">
                학교급별 사고 수 월별 5개년 누적 비교
                </h4>
                ''', unsafe_allow_html=True)
    st.plotly_chart(create_stacked_barchart(month_level_pivot, sch_type_cat, colors, months))
    
    st.markdown('######')
    st.markdown('학교급마다 월별로 발생한 총 사고 수를 5개년 누적하여 비교하였습니다. 특정 학교급에서 어느 달에 사고가 가장 많이 발생했는지 양상을 파악할 수 있습니다.', unsafe_allow_html=True)
    st.markdown('초등학교의 경우에는 저학년과 고학년의 특성이 서로 다르다고 보아 이를 구분해 분석하였습니다.', unsafe_allow_html=True)

    st.divider()

    col = st.columns((0.5, 5, 0.5), gap='medium')
with col[1]:
    st.markdown('######')
    st.markdown(f'''
                <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0; text-align: center;">
                학교급별 사고 내용 5개년 누적 분석
                </h4>
                ''', unsafe_allow_html=True)
st.markdown('###')

st.markdown('학교급별 사고 내용(사고 시간, 사고 장소, 사고 부위, 사고 형태, 사고 당시 활동, 사고 매개물)에 대한 정보를 5개년 통합하여 제공합니다. 분석 결과 중 상위 5개 항목만 제공하여 특정 학교급에서의 주된 사고 발생 양상을 파악할 수 있습니다.', unsafe_allow_html=True)
st.markdown('초등학교의 경우에는 저학년과 고학년의 특성이 서로 다르다고 보아 이를 구분해 분석하였습니다.', unsafe_allow_html=True)
st.divider()
        
# 탭 정의
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["사고 시간", "사고 장소", "사고 부위", "사고 형태", "사고 당시 활동", "사고 매개물"])

# 학교급 정렬 기준 지정
custom_order = ["유치원", "초등학교(저학년)", "초등학교(고학년)", "중학교", "고등학교", "특수학교"]

# sch_acci_time 데이터프레임(사고시간 5개년 누적)
# '학교급'의 '기타학교' 값 제외
sch_acci_time = sch_df[sch_df['학교급'] != '기타학교']
# 초등학교 저학년/고학년 구분
sch_acci_time.loc[(sch_acci_time['학교급']=='초등학교')&(sch_acci_time['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등학교(저학년)'
sch_acci_time.loc[(sch_acci_time['학교급']=='초등학교')&(sch_acci_time['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등학교(고학년)'
# 분석 편의를 위해 일부 데이터 값 변경
sch_acci_time = sch_acci_time.replace('점심시간', '식사시간')
sch_acci_time = sch_acci_time.replace('석식시간', '식사시간')
sch_acci_time = sch_acci_time.replace('휴식시간 및 청소시간', '휴식/청소시간')
# 연도, 학교급, 사고시간별 사고수 계산
sch_acci_time = sch_acci_time.groupby(['학교급', '사고시간']).size().reset_index(name='사고수')
# 학교급 기준으로 정렬
sch_acci_time['학교급'] = pd.Categorical(sch_acci_time['학교급'], categories=custom_order, ordered=True)
sch_acci_time = sch_acci_time.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)
# 초등학교 저학년/고학년 구분 과정에서 생긴 nan 값(사고자학년 값이 유아인 경우) 처리
sch_acci_time = sch_acci_time.dropna()

# sch_acci_place 데이터프레임(사고장소 5개년 누적)
# '학교급'의 '기타학교' 값 제외
sch_acci_place = sch_df[sch_df['학교급'] != '기타학교']
# 초등학교 저학년/고학년 구분
sch_acci_place.loc[(sch_acci_place['학교급']=='초등학교')&(sch_acci_place['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등학교(저학년)'
sch_acci_place.loc[(sch_acci_place['학교급']=='초등학교')&(sch_acci_place['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등학교(고학년)'
# 분석 편의를 위해 일부 데이터 값 변경
sch_acci_place = sch_acci_place.replace('교외활동', '교외')
# 연도, 학교급, 사고장소별 사고수 계산
sch_acci_place = sch_acci_place.groupby(['학교급', '사고장소']).size().reset_index(name='사고수')
# 학교급 기준으로 정렬
sch_acci_place['학교급'] = pd.Categorical(sch_acci_place['학교급'], categories=custom_order, ordered=True)
sch_acci_place = sch_acci_place.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)
# 초등학교 저학년/고학년 구분 과정에서 생긴 nan 값(사고자학년 값이 유아인 경우) 처리
sch_acci_place = sch_acci_place.dropna()

# sch_acci_part 데이터프레임(사고부위 5개년 누적)
# '학교급'의 '기타학교' 값 제외
sch_acci_part = sch_df[sch_df['학교급'] != '기타학교']
# 초등학교 저학년/고학년 구분
sch_acci_part.loc[(sch_acci_part['학교급']=='초등학교') & (sch_acci_part['사고자학년'].isin(['1학년','2학년','3학년'])), '학교급'] = '초등학교(저학년)'
sch_acci_part.loc[(sch_acci_part['학교급']=='초등학교') & (sch_acci_part['사고자학년'].isin(['4학년','5학년','6학년'])), '학교급'] = '초등학교(고학년)'
# 분석 편의를 위해 일부 데이터 값 변경
sch_acci_part['사고부위'] = sch_acci_part['사고부위'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()
# 연도, 학교급, 사고부위별 사고수 계산
sch_acci_part = sch_acci_part.groupby(['학교급', '사고부위']).size().reset_index(name='사고수')
# 학교급 기준으로 정렬
sch_acci_part['학교급'] = pd.Categorical(sch_acci_part['학교급'], categories=custom_order, ordered=True)
sch_acci_part = sch_acci_part.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)
# 초등학교 저학년/고학년 구분 과정에서 생긴 nan 값(사고자학년 값이 유아인 경우) 처리
sch_acci_part = sch_acci_part.dropna()

# sch_acci_type 데이터프레임(사고형태 5개년 누적)
# '학교급'의 '기타학교' 값 제외
sch_acci_type = sch_df[sch_df['학교급'] != '기타학교']
# 초등학교 저학년/고학년 구분
sch_acci_type.loc[(sch_acci_type['학교급']=='초등학교') & (sch_acci_type['사고자학년'].isin(['1학년','2학년','3학년'])), '학교급'] = '초등학교(저학년)'
sch_acci_type.loc[(sch_acci_type['학교급']=='초등학교') & (sch_acci_type['사고자학년'].isin(['4학년','5학년','6학년'])), '학교급'] = '초등학교(고학년)'
# 분석 편의를 위해 일부 데이터 값 변경
sch_acci_type = sch_acci_type.replace('낙상-미끄러짐', '낙상')
sch_acci_type = sch_acci_type.replace('낙상-넘어짐', '낙상')
sch_acci_type = sch_acci_type.replace('낙상-떨어짐', '낙상')
sch_acci_type = sch_acci_type.replace('염좌·삐임 등 신체 충격', '신체 충격')
# 연도, 학교급, 사고형태별 사고수 계산
sch_acci_type = sch_acci_type.groupby(['학교급', '사고형태']).size().reset_index(name='사고수')
# 학교급 기준으로 정렬
sch_acci_type['학교급'] = pd.Categorical(sch_acci_type['학교급'], categories=custom_order, ordered=True)
sch_acci_type = sch_acci_type.sort_values(['학교급', '사고수'], ascending=[True, False]).reset_index(drop=True)
# 초등학교 저학년/고학년 구분 과정에서 생긴 nan 값(사고자학년 값이 유아인 경우) 처리
sch_acci_type = sch_acci_type.dropna()

# sch_acci_act 데이터프레임(사고당시활동 5개년 누적)
# '학교급'의 '기타학교' 값 제외
sch_acci_act = sch_df[sch_df['학교급'] != '기타학교']
# 초등학교 저학년/고학년 구분
sch_acci_act.loc[(sch_acci_act['학교급']=='초등학교') & (sch_acci_act['사고자학년'].isin(['1학년','2학년','3학년'])), '학교급'] = '초등학교(저학년)'
sch_acci_act.loc[(sch_acci_act['학교급']=='초등학교') & (sch_acci_act['사고자학년'].isin(['4학년','5학년','6학년'])), '학교급'] = '초등학교(고학년)'
# 연도, 학교급, 사고당시활동별 사고수 계산
sch_acci_act = sch_acci_act.groupby(['학교급', '사고당시활동']).size().reset_index(name='사고수')
# 연도, 학교급 기준으로 정렬
sch_acci_act['학교급'] = pd.Categorical(sch_acci_act['학교급'], categories=custom_order, ordered=True)
sch_acci_act = sch_acci_act.sort_values(['학교급', '사고수']).reset_index(drop=True)
# 초등학교 저학년/고학년 구분 과정에서 생긴 nan 값(사고자학년 값이 유아인 경우) 처리
sch_acci_act = sch_acci_act.dropna()

# sch_acci_mdm 데이터프레임(사고매개물 5개년 누적)
# '학교급'의 '기타학교' 값 제외
sch_acci_mdm = sch_df[sch_df['학교급'] != '기타학교']
# 초등학교 저학년/고학년 구분
sch_acci_mdm.loc[(sch_acci_mdm['학교급']=='초등학교') & (sch_acci_mdm['사고자학년'].isin(['1학년','2학년','3학년'])), '학교급'] = '초등학교(저학년)'
sch_acci_mdm.loc[(sch_acci_mdm['학교급']=='초등학교') & (sch_acci_mdm['사고자학년'].isin(['4학년','5학년','6학년'])), '학교급'] = '초등학교(고학년)'
# 분석 편의를 위해 일부 데이터 값 변경
sch_acci_mdm['사고매개물'] = sch_acci_mdm['사고매개물'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()
# 연도, 학교급, 사고매개물별 사고수 계산
sch_acci_mdm = sch_acci_mdm.groupby(['학교급', '사고매개물']).size().reset_index(name='사고수')
# 연도, 학교급 기준으로 정렬
sch_acci_mdm['학교급'] = pd.Categorical(sch_acci_mdm['학교급'], categories=custom_order, ordered=True)
sch_acci_mdm = sch_acci_mdm.sort_values(['학교급', '사고수']).reset_index(drop=True)
# 초등학교 저학년/고학년 구분 과정에서 생긴 nan 값(사고자학년 값이 유아인 경우) 처리
sch_acci_mdm = sch_acci_mdm.dropna()

# 그래프 색 지정
colors = {
    "유치원": '#5c7dd2', 
    "초등학교(저학년)": '#92b8ff', 
    "초등학교(고학년)": '#aeceff', 
    "중학교": '#c7e4ff', 
    "고등학교": '#c3b7eb', 
    "특수학교": '#9590e6'
    }

# 사고 시간 탭
with tab1:
    st.markdown('######')
    st.markdown(f'''
        <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
        학교급별 사고 시간
        </h4>
        ''', unsafe_allow_html=True)
    
    # sch_acci_time 그래프 시각화
    st.plotly_chart(create_sub_barchart(sch_acci_time, '사고시간', '사고수', colors))

# 사고 장소 탭
with tab2:
    st.markdown('######')
    st.markdown(f'''
        <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
        학교급별 사고 장소
        </h4>
        ''', unsafe_allow_html=True)
    
    # sch_acci_place 그래프 시각화
    st.plotly_chart(create_sub_barchart(sch_acci_place, '사고장소', '사고수', colors))

# 사고 부위 탭
with tab3:
    st.markdown('######')
    st.markdown(f'''
        <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
        학교급별 사고 부위
        </h4>
        ''', unsafe_allow_html=True)
    
    # sch_acci_part 그래프 시각화
    st.plotly_chart(create_sub_barchart(sch_acci_part, '사고부위', '사고수', colors))

# 사고 형태 탭
with tab4:
    st.markdown('######')
    st.markdown(f'''
        <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
        학교급별 사고 형태
        </h4>
        ''', unsafe_allow_html=True)
    
    # sch_acci_type 그래프 시각화
    st.plotly_chart(create_sub_barchart(sch_acci_type, '사고형태', '사고수', colors))

# 사고 당시 활동 탭
with tab5:
    st.markdown('######')
    st.markdown(f'''
        <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
        학교급별 사고 당시 활동
        </h4>
        ''', unsafe_allow_html=True)
    
    # sch_acci_act 그래프 시각화
    st.plotly_chart(create_sub_barchart(sch_acci_act, '사고당시활동', '사고수', colors))

# 사고 매개물 탭
with tab6:
    st.markdown('######')
    st.markdown(f'''
        <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
        학교급별 사고 매개물
        </h4>
        ''', unsafe_allow_html=True)
    
    # sch_acci_mdm 그래프 시각화
    st.plotly_chart(create_sub_barchart(sch_acci_mdm, '사고매개물', '사고수', colors))                
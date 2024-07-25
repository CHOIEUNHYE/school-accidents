# 사고 내용 분석 streamlit 파일
import streamlit as st
import pandas as pd
import polars as pl
import os
from function.function_acc_detail import *  # function.py 파일에서 모든 함수 불러오기 

# 현재 파일의 디렉토리를 기준으로 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))

# 폰트 설정
with open( current_dir+"/component/style/KoPubWorld Dotum.css" ) as css:
    st.write( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

with open( current_dir+"/component/style/style.css" ) as css:
    st.write( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

#######################
#데이터 불러오기

df = pl.read_csv(current_dir +'/component/data/학교안전사고데이터통합/학교안전사고데이터_5개년통합_월계절추가.csv')
df = df.to_pandas()
df['사고발생일'] = pd.to_datetime(df['사고발생일'])
df['연도'] = df['사고발생일'].map(lambda x : x.year)


# 데이터 전처리
df_2019 = df[df['사고발생일'].between('2019-01-01', '2019-12-31')]
df_2020 = df[df['사고발생일'].between('2020-01-01', '2020-12-31')]
df_2021 = df[df['사고발생일'].between('2021-01-01', '2021-12-31')]
df_2022 = df[df['사고발생일'].between('2022-01-01', '2022-12-31')]
df_2023 = df[df['사고발생일'].between('2023-01-01', '2023-12-31')]


st.markdown('''
<h1 style="font-family: 'KoPubWorld Dotum', sans-serif; text-align: center;">
    학교안전사고 내용 분석
</h1>
''', unsafe_allow_html=True)

st.markdown('######')
st.write('''발생한 학교안전사고의 구체적인 내용에 대한 정보를 제공합니다. 사고와 관련하여 사고가 언제 어디에서 많이 발생했는지, 사고 당시 어떤 활동을 하고 있었는지 등
            구체적인 안전사고의 내용에 대한 교차분석 결과를 확인할 수 있습니다. 그래프에서 구체적인 정보를 확인하고 싶은 항목에 마우스 커서를 올리면 해당 항목에 대한 정보를 확인할 수 있습니다.''')

st.markdown('######')

st.markdown('''
<h2 style="font-family: 'KoPubWorld Dotum', sans-serif;">
    장소별 안전사고 발생 현황
</h2>
''', unsafe_allow_html=True)
st.write('2019년~2023년 5개년간의 학교 장소별 안전사고 발생 현황에 대한 정보를 제공합니다. 다양한 장소의 특성에 따른 안전사고 발생 현황을 상세히 확인할 수 있습니다.')
# 레이아웃 나누기 : 1 대 5 화면 비율 나눈 거임!!
col = st.columns((1, 5), gap='medium')


with col[0] :
    st.markdown('''
    <h4 style="font-family: 'KoPubWorld Dotum', sans-serif;">
    2023년 하루 평균<br> 발생 안전사고 수
    </h4>
    ''', unsafe_allow_html=True)
    acc_spot_oneday_2023 = df_2023.groupby(['사고장소']).count()[['구분']].reset_index().sort_values('구분',ascending=False)
    acc_spot_oneday_2023['하루평균발생사고수'] = round(acc_spot_oneday_2023['구분']/365,1)
    acc_spot_oneday_2023.columns = ['사고장소','총사고수','하루평균발생사고수']
    
    for i in range(0,5):
        st.metric(label=acc_spot_oneday_2023.iloc[i,0],value=str(acc_spot_oneday_2023.iloc[i,2])+'건')

with col[1] :
    
    acc_spot_2019 = get_grouped_count_spot(df_2019,'사고장소',2019).replace('교외활동','교외')
    acc_spot_2020 = get_grouped_count_spot(df_2020,'사고장소',2020).replace('교외활동','교외')
    acc_spot_2021 = get_grouped_count_spot(df_2021,'사고장소',2021).replace('교외활동','교외')
    acc_spot_2022 = get_grouped_count_spot(df_2022,'사고장소',2022).replace('교외활동','교외')
    acc_spot_2023 = get_grouped_count_spot(df_2023,'사고장소',2023).replace('교외활동','교외')
    acc_spot = pd.concat([acc_spot_2019,acc_spot_2020,acc_spot_2021,acc_spot_2022,acc_spot_2023]).reset_index(drop=True)
    

    # st.markdown('#####')
    ## 탭 만들기
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["5개년 전체","2019년", "2020년", "2021년", "2022년","2023년"])
    ## 탭별 차트 그리기
    def acc_spot_chart_oneyear(one_year_df):
        col = st.columns((4.5,3), gap='medium')
        with col[0] :
            st.markdown('###')
            acc_spot_oneyear_fig = horizontal_chart_one_year(one_year_df,'사고장소')
            st.plotly_chart(acc_spot_oneyear_fig, theme="streamlit", use_container_width=True)
        with col[1] :
            st.markdown('##')
            st.markdown('##')
            st.markdown('###')
            print_df = one_year_df.sort_values(['연도','사고건수'],ascending=[True,False]).reset_index(drop=True)
            print_df['퍼센트'] = print_df['퍼센트'].astype(str)
            styled_df = style_dataframe(print_df[['연도','사고장소','사고건수','퍼센트']]).hide(axis='index')
            html_df = styled_df.to_html()
            st.write(html_df, unsafe_allow_html=True)               
            # st.dataframe(print_df[['연도','사고장소','사고건수','퍼센트']])

    with tab1:
        col = st.columns((4.5, 3), gap='medium')
        with col[0] : 
            st.markdown('######')
            acc_spot_chart = acc_spot_5years_chart(acc_spot)
            st.plotly_chart(acc_spot_chart, theme="streamlit", use_container_width=True)
        with col[1] :
            st.markdown('##')
            st.markdown('###')
            print_df = acc_spot.sort_values(['연도','사고건수'],ascending=[True,False]).reset_index(drop=True)
            print_df['퍼센트'] = print_df['퍼센트'].astype(str)
            styled_df = style_dataframe(print_df[['연도','사고장소','사고건수','퍼센트']]).hide(axis='index')
            html_df = styled_df.to_html()
            st.write(html_df, unsafe_allow_html=True)                 

    with tab2:
        acc_spot_chart_oneyear(acc_spot_2019)
    with tab3:
        acc_spot_chart_oneyear(acc_spot_2020)
    with tab4:
        acc_spot_chart_oneyear(acc_spot_2021)
    with tab5:
        acc_spot_chart_oneyear(acc_spot_2022)
    with tab6:
        acc_spot_chart_oneyear(acc_spot_2023)

st.markdown('##')
st.subheader('장소에 따른 사고부위 및 사고당시활동')
st.write('''사고 장소에 따라 사고부위와 사고당시활동 양상이 어떻게 달라지는지에 대한 정보를 제공합니다. 각 장소에서 학생들이 어떤 부위를 많이 다치는지, 어떤 활동을 하다가 다치는지를 확인할 수 있습니다.
            안전사고 발생 시 가장 많이 다치는 사고부위 상위 5개 항목과 안전사고 발생이 많은 활동 상위 5개 항목이 제공됩니다.
            ''')
tab = st.tabs(['사고부위','사고당시활동'])
with tab[0]:

    df['사고장소'] = df['사고장소'].str.replace('교외활동','교외')
    df['사고부위'] = df['사고부위'].str.replace('머리\(두부\)','머리')
    acc_body = df.groupby(['사고장소','사고부위']).count()[['구분']].reset_index().sort_values('구분')
    spot_body_chart = spot_body_fig(acc_body)
    st.plotly_chart(spot_body_chart, theme="streamlit", use_container_width=True)
with tab[1]:
    df['사고장소'] = df['사고장소'].str.replace('교외활동','교외')
    acc_activity = df[df['연도']!=2023].groupby(['사고장소','사고당시활동']).count()[['구분']].reset_index().sort_values('구분')
    spot_activity_chart = spot_activity_fig(acc_activity)
    st.plotly_chart(spot_activity_chart, theme="streamlit")

st.divider() ## 구분선

st.markdown('''
<h2 style="font-family: 'KoPubWorld Dotum', sans-serif;">
    시간별 안전사고 발생 현황
</h2>
''', unsafe_allow_html=True)
st.write('''2019년~2023년 5개년간의 시간별 안전사고 발생 현황에 대한 정보를 제공합니다. 
            사고가 발생한 월, 계절, 학교에서의 특정 활동 시간과 같이 다양한 시간 범주에 따른 안전사고 발생 현황을 상세히 확인할 수 있습니다. ''')

time_df=df.copy()
time_df.loc[(time_df['학교급']=='초등학교')&(time_df['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등학교(저학년)'
time_df.loc[(time_df['학교급']=='초등학교')&(time_df['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등학교(고학년)'

acc_month = time_df.groupby('사고월').count()[['구분']].reset_index()
acc_month.columns = ['사고월','사고건수']
months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]

# pd.Categorical을 사용하여 순서를 지정하고, sort_values를 적용
acc_month['사고월'] = pd.Categorical(acc_month['사고월'], categories=months, ordered=True)
acc_month.sort_values('사고월',inplace=True)

col = st.columns([5,4.5], gap='medium')

with col[0] :
    st.markdown("""
        <h3 style="text-align: center;">월별 누적 안전사고 수(2019~2023)</h3>
        """, unsafe_allow_html=True)
    acc_time_chart = acc_month_fig(acc_month)
    st.plotly_chart(acc_time_chart, theme="streamlit", use_container_width=True)
    

with col[1] : 
    st.markdown("""
        <h3 style="text-align: center;">장소에 따른 월별 안전사고 수(2019~2023)</h3>
        """, unsafe_allow_html=True)
    # 각 사고월별 총 사고 건수 계산
    total_by_school = time_df.groupby('사고월')['구분'].count()
    # 사고월에 따른 사고장소별 사고건수 카운트
    month_spot = time_df.groupby(['사고월','사고장소'])[['구분']].count().reset_index()
    
    # 각 행에 대해 퍼센트를 계산하여 새로운 컬럼 추가
    month_spot['퍼센트'] = month_spot.apply(lambda row:round((row['구분'] / total_by_school[row['사고월']]) * 100,1), axis=1)
    month_spot.columns = ['사고월','사고장소','사고건수','퍼센트']
    month_spot_chart = month_spot_fig(month_spot)
    st.plotly_chart(month_spot_chart, theme=None, use_container_width=True)

st.subheader('계절별 안전사고부위')
st.write('''계절에 따른 사고부위 양상에 대한 정보를 제공합니다. 계절별로 학생들이 많이 다치는 부위를 확인하고 적절한 계절별 안전사고 예방 대책을 고안할 수 있습니다. 2019년~2023년 5개년 누적으로 사고 수를 집계하였습니다.''')
season_body = time_df.groupby(['계절','사고부위']).count()[['구분']].reset_index()
season_body.columns = ['계절','사고부위','사고건수']
season_order = ["봄", "여름", "가을", "겨울"]
season_body['계절'] = pd.Categorical(season_body['계절'], categories=season_order, ordered=True)
season_body.sort_values(['계절','사고건수'],inplace=True)
season_body_chart = season_body_fig(season_body)
st.plotly_chart(season_body_chart, theme="streamlit", use_container_width=True)

st.subheader('계절별 사고당시활동')
st.write('''계절에 따른 사고당시활동의 양상에 대한 정보를 제공합니다. 계절별로 학생들이 어떤 활동을 하다가 주로 다치는지를 확인하고 적절한 계절별 안전사고 예방 대책을 고안할 수 있습니다. 2019년~2023년 5개년 누적으로 사고 수를 집계하였습니다.''')
season_activity = time_df.groupby(['계절','사고당시활동']).count()[['구분']].reset_index()
season_activity.columns = ['계절','사고당시활동','사고건수']
season_order = ["봄", "여름", "가을", "겨울"]
season_activity['계절'] = pd.Categorical(season_activity['계절'], categories=season_order, ordered=True)
season_activity.sort_values(['계절','사고건수'],inplace=True)
season_activity_chart = season_activity_fig(season_activity)
st.plotly_chart(season_activity_chart, theme="streamlit", use_container_width=True)

st.markdown('###')
col = col = st.columns([3,3])
with col[0]:
    st.subheader('사고시간 워드클라우드')
    st.write('학교안전사고가 발생한 시간에 대한 정보를 워드클라우드로 제공합니다. 학교안전사고가 많이 발생하는 시간일수록 단어의 크기가 커집니다. 2019년~2023년 5개년 누적으로 사고 수를 집계하였습니다.')
    st.markdown('#####')
    st.image(current_dir+'/component/img/워드클라우드3.png')
with col[1]:
    # 카테고리를 수정함, 같은 카테고리로 묶일 수 있는 항목을 묶어줌
    acc_time = time_df.groupby('사고시간').count()[['구분']].reset_index().sort_values('구분')
    acc_time.columns = ['사고시간','사고건수']
    acc_time_analysis = acc_time.replace('체육수업','체육활동').replace('석식시간','식사시간').replace('점심시간','식사시간').replace('쉬는시간','휴식시간 및 청소시간').groupby('사고시간').sum()[['사고건수']].reset_index().sort_values('사고건수')    
    
    acc_time_chart = acc_time_top5_fig(acc_time_analysis)
    st.subheader('학교안전사고발생 시간 TOP 5')
    st.markdown('학교안전사고가 많이 발생한 학교 활동 시간 상위 5개의 항목을 제공합니다. 비슷한 시간 분류의 경우 하나의 분류로 묶어서 집계했습니다. (예시: [체육수업, 체육활동] => 체육활동으로 통일)', unsafe_allow_html=True)
    st.plotly_chart(acc_time_chart, theme="streamlit", use_container_width=True)

## 안전사고 발생 Top 5 사고시간 데이터만 추출
time_analysis_df = time_df.replace('체육수업','체육활동').replace('석식시간','식사시간').replace('점심시간','식사시간').replace('쉬는시간','휴식시간 및 청소시간')
time_analysis_other_df = time_analysis_df[time_analysis_df['사고시간'].isin(['체육활동','식사시간','휴식시간 및 청소시간','수업시간','학교행사'])]
time_analysis_how_df = time_analysis_other_df.groupby(['사고시간','사고당시활동']).count()[['구분']].reset_index()
time_tree_map_chart = time_tree_map(time_analysis_how_df)
st.markdown('######')
st.subheader('사고시간별 사고 당시 활동 분포')
st.markdown('학교안전사고가 많이 발생한 시간 상위 5개의 항목에 대해 사고 당시 활동의 분포에 대한 정보를 제공합니다. 학교안전사고가 발생한 시간별로 사고의 원인이 되는 활동의 분포를 확인할 수 있습니다. 그래프에서 특정 시간 항목을 선택할 경우 해당 시간만을 기준으로 하여 사고 당시 활동의 분포를 확인할 수 있습니다.', unsafe_allow_html=True)
st.plotly_chart(time_tree_map_chart, theme="streamlit", use_container_width=True)

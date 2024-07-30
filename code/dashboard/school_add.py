# 추가 분석 streamlit 파일
import streamlit as st
import pandas as pd
import polars as pl
from function_school_add import *  # function_school_add.py 파일에서 모든 함수 불러오기 

# 폰트 설정
with open( "component\style\KoPubWorld Dotum.css" ) as css:
    st.write( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

with open( "component\style\style.css" ) as css:
    st.write( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

#######################
#데이터 불러오기

df = pl.read_csv('../../../school-accidents/code/dashboard/component/data/sch_df_addage.csv')
df = df.to_pandas()

st.markdown('''
<h1 style="font-family: 'KoPubWorld Dotum', sans-serif; text-align: center;">
    학교안전사고 추가 관계 분석
</h1>
''', unsafe_allow_html=True)

st.markdown('######')
st.write('나이, 학교급, 사고 수, 사고 내용 간의 관계에 대한 정보를 추가 제공합니다.')
st.markdown('안전사고 중 학생이 당한 사고에 초점을 맞춰 분석 시 사고자구분 값 중 일반학생, 특수학교(학급)학생, 체육특기학생만을 대상으로 하였습니다.<br>앞서 언급한 컬럼 간의 연관성 정도를 분석하기 위해서는 상관 분석, 히트맵, 박스플롯을 활용하였습니다.', unsafe_allow_html=True)
st.markdown('######')     

st.divider()

# 레이아웃 설정
col = st.columns((1, 2.5, 0.5, 2.5, 1), gap='medium')

# sch_totacci 데이터프레임(5개년 누적, 초등학교 저학년/고학년 구분)
sch_totacci = df[df['학교급'].isin(['기타학교', '특수학교'])]
# 초등학교 저학년/고학년 구분
sch_totacci.loc[(sch_totacci['학교급']=='초등학교')&(sch_totacci['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등(저)'
sch_totacci.loc[(sch_totacci['학교급']=='초등학교')&(sch_totacci['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등(고)'
# 학교급 기준으로 groupby
sch_totacci = sch_totacci.groupby(['학교급']).size().reset_index(name='총 사고수')
# 시각화 편의를 위해 중학교, 고등학교 값 변경
sch_totacci['학교급'] = sch_totacci['학교급'].replace({'중학교': '중등', '고등학교': '고등'})
# 학교급 기준으로 정렬
custom_order = ["유치원", "초등(저)", "초등(고)", "중등", "고등"]
sch_totacci['학교급'] = pd.Categorical(sch_totacci['학교급'], categories=custom_order, ordered=True)
sch_totacci = sch_totacci.sort_values(['학교급']).reset_index(drop=True)
# 초등학교 저학년/고학년 구분 과정에서 생긴 nan 값(사고자학년 값이 유아인 경우) 처리
sch_totacci = sch_totacci.dropna()

# age_totacci 데이터프레임(5개년 누적, 나이 컬럼 활용)
# '학교급'의 '유치원', '특수학교', '기타학교' 값 제외
age_totacci = df[
    (df['학교급'] != '유치원') &
    (df['학교급'] != '특수학교') &
    (df['학교급'] != '기타학교') 
    ]
# '초등학교'의 '사고자학년'에서 '유아' 값을 제외
age_totacci = age_totacci[~((age_totacci['학교급'] == '초등학교') & 
                            (age_totacci['사고자학년'] == '유아'))]
# '중학교'의 '사고자학년'에서 '4학년'과 '5학년' 값을 제외
age_totacci = age_totacci[~((age_totacci['학교급'] == '중학교') & 
                            ((age_totacci['사고자학년'] == '4학년') | 
                             (age_totacci['사고자학년'] == '5학년')))]
# '나이'가 0인 행 추가 제거
age_totacci = age_totacci[age_totacci['나이'] != 0]
# 사고자학년_수정 기준으로 groupby
age_totacci = age_totacci.groupby(['나이', '사고자학년_수정']).size().reset_index(name='총 사고수')
# 사고자학년_수정 기준으로 정렬
custom_order = [
    '초등_1학년', '초등_2학년', '초등_3학년', '초등_4학년', '초등_5학년', '초등_6학년',
    '중등_1학년', '중등_2학년', '중등_3학년', 
    '고등_1학년', '고등_2학년', '고등_3학년'
    ]
age_totacci['사고자학년_수정'] = pd.Categorical(age_totacci['사고자학년_수정'], categories=custom_order, ordered=True)
age_totacci = age_totacci.sort_values(['나이', '사고자학년_수정']).reset_index(drop=True)
    
with col[1]:
    # sch_totacci 분석 결과 시각화
    st.markdown('###')
    st.markdown(f'''
                <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
                학교급과 사고 수 간의 관계 분석
                </h4>
                ''', unsafe_allow_html=True)
    custom_order = ["고등", "중등", "초등(고)", "초등(저)", "유치원"]
    st.plotly_chart(create_h_barchart(sch_totacci, '총 사고수', '학교급', custom_order))
    
with col[3]:
    # age_totacci 분석 결과 시각화
    st.markdown('###')
    st.markdown(f'''
                <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
                나이와 사고 수 간의 관계 분석
                </h4>
                ''', unsafe_allow_html=True)
    st.plotly_chart(create_line_chart(age_totacci, '나이', '총 사고수'))
    
st.divider()

st.markdown('######')
st.markdown(f'''
            <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0; text-align: center;">
            학교급 또는 나이와 사고 내용 간의 관계 분석
            </h4>
            ''', unsafe_allow_html=True)
st.markdown('###')

# 탭 정의
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["사고 시간", "사고 장소", "사고 부위", "사고 형태", "사고 당시 활동", "사고 매개물"])

# 학교급 정렬 기준 지정
custom_order = ["유치원", "초등(저)", "초등(고)", "중등", "고등"]

# sch_accitime 데이터프레임(5개년 누적)
# '학교급'의 '특수학교', '기타학교' 값 제외
sch_accitime = df[
    (df['학교급'] != '특수학교') &
    (df['학교급'] != '기타학교')
    ]
# 초등학교 저학년/고학년 구분
sch_accitime.loc[(sch_accitime['학교급']=='초등학교')&(sch_accitime['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등(저)'
sch_accitime.loc[(sch_accitime['학교급']=='초등학교')&(sch_accitime['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등(고)'
# 초등학교 중 유아인 행을 제거
sch_accitime = sch_accitime[sch_accitime['학교급'] != '초등학교']
# '학교급'과 '사고시간' 컬럼 선택
sch_accitime = sch_accitime[['학교급', '사고시간']]
# 분석 편의를 위해 일부 데이터 값 변경
sch_accitime = sch_accitime.replace('점심시간', '식사시간')
sch_accitime = sch_accitime.replace('석식시간', '식사시간')
sch_accitime = sch_accitime.replace('휴식시간 및 청소시간', '휴식/청소시간')
# 시각화 편의를 위해 중학교, 고등학교 값 변경
sch_accitime['학교급'] = sch_accitime['학교급'].replace({'중학교': '중등', '고등학교': '고등'})
# 컬럼명 변경
sch_accitime.rename(columns={'사고시간': '사고 시간'}, inplace=True)

# sch_acciplace 데이터프레임(5개년 누적)
# '학교급'의 '특수학교', '기타학교' 값 제외
sch_acciplace = df[
    (df['학교급'] != '특수학교') &
    (df['학교급'] != '기타학교')
    ]
# 초등학교 저학년/고학년 구분
sch_acciplace.loc[(sch_acciplace['학교급']=='초등학교')&(sch_acciplace['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등(저)'
sch_acciplace.loc[(sch_acciplace['학교급']=='초등학교')&(sch_acciplace['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등(고)'
# 초등학교 중 유아인 행을 제거
sch_acciplace = sch_acciplace[sch_acciplace['학교급'] != '초등학교']
# '학교급'과 '사고장소' 컬럼 선택
sch_acciplace = sch_acciplace[['학교급', '사고장소']]
# 분석 편의를 위해 일부 데이터 값 변경
sch_acciplace = sch_acciplace.replace('교외활동', '교외')
# 시각화 편의를 위해 중학교, 고등학교 값 변경
sch_acciplace['학교급'] = sch_acciplace['학교급'].replace({'중학교': '중등', '고등학교': '고등'})
# 컬럼명 변경
sch_acciplace.rename(columns={'사고장소': '사고 장소'}, inplace=True)

# sch_accipart 데이터프레임(5개년 누적)
# '학교급'의 '특수학교', '기타학교' 값 제외
sch_accipart = df[
    (df['학교급'] != '특수학교') &
    (df['학교급'] != '기타학교')
    ]
# 초등학교 저학년/고학년 구분
sch_accipart.loc[(sch_accipart['학교급']=='초등학교')&(sch_accipart['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등(저)'
sch_accipart.loc[(sch_accipart['학교급']=='초등학교')&(sch_accipart['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등(고)'
# 초등학교 중 유아인 행을 제거
sch_accipart = sch_accipart[sch_accipart['학교급'] != '초등학교']
# '학교급'과 '사고부위' 컬럼 선택
sch_accipart = sch_accipart[['학교급', '사고부위']]
# 분석 편의를 위해 일부 데이터 값 변경
sch_accipart['사고부위'] = sch_accipart['사고부위'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()
# 시각화 편의를 위해 중학교, 고등학교 값 변경
sch_accipart['학교급'] = sch_accipart['학교급'].replace({'중학교': '중등', '고등학교': '고등'})
# 컬럼명 변경
sch_accipart.rename(columns={'사고부위': '사고 부위'}, inplace=True)

# sch_accitype 데이터프레임(5개년 누적)
# '학교급'의 '특수학교', '기타학교' 값 제외
sch_accitype = df[
    (df['학교급'] != '특수학교') &
    (df['학교급'] != '기타학교')
    ]
# 초등학교 저학년/고학년 구분
sch_accitype.loc[(sch_accitype['학교급']=='초등학교')&(sch_accitype['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등(저)'
sch_accitype.loc[(sch_accitype['학교급']=='초등학교')&(sch_accitype['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등(고)'
# 초등학교 중 유아인 행을 제거
sch_accitype = sch_accitype[sch_accitype['학교급'] != '초등학교']
# '학교급'과 '사고형태' 컬럼 선택
sch_accitype = sch_accitype[['학교급', '사고형태']]
# 분석 편의를 위해 일부 데이터 값 변경
sch_accitype = sch_accitype.replace('낙상-미끄러짐', '낙상')
sch_accitype = sch_accitype.replace('낙상-넘어짐', '낙상')
sch_accitype = sch_accitype.replace('낙상-떨어짐', '낙상')
sch_accitype = sch_accitype.replace('염좌·삐임 등 신체 충격', '신체 충격')
# 시각화 편의를 위해 중학교, 고등학교 값 변경
sch_accitype['학교급'] = sch_accitype['학교급'].replace({'중학교': '중등', '고등학교': '고등'})
# 컬럼명 변경
sch_accitype.rename(columns={'사고형태': '사고 형태'}, inplace=True)

# sch_acciact 데이터프레임(5개년 누적)
# '학교급'의 '특수학교', '기타학교' 값 제외
sch_acciact = df[
    (df['학교급'] != '특수학교') &
    (df['학교급'] != '기타학교')
    ]
# 초등학교 저학년/고학년 구분
sch_acciact.loc[(sch_acciact['학교급']=='초등학교')&(sch_acciact['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등(저)'
sch_acciact.loc[(sch_acciact['학교급']=='초등학교')&(sch_acciact['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등(고)'
# 초등학교 중 유아인 행을 제거
sch_acciact = sch_acciact[sch_acciact['학교급'] != '초등학교']
# '학교급'과 '사고당시활동' 컬럼 선택
sch_acciact = sch_acciact[['학교급', '사고당시활동']]
# 시각화 편의를 위해 중학교, 고등학교 값 변경
sch_acciact['학교급'] = sch_acciact['학교급'].replace({'중학교': '중등', '고등학교': '고등'})
# 컬럼명 변경
sch_acciact.rename(columns={'사고당시활동': '사고 당시 활동'}, inplace=True)

# sch_accimdm 데이터프레임(5개년 누적)
# '학교급'의 '특수학교', '기타학교' 값 제외
sch_accimdm = df[
    (df['학교급'] != '특수학교') &
    (df['학교급'] != '기타학교')
    ]
# 초등학교 저학년/고학년 구분
sch_accimdm.loc[(sch_accimdm['학교급']=='초등학교')&(sch_accimdm['사고자학년'].isin(['1학년','2학년','3학년'])),'학교급']='초등(저)'
sch_accimdm.loc[(sch_accimdm['학교급']=='초등학교')&(sch_accimdm['사고자학년'].isin(['4학년','5학년','6학년'])),'학교급']='초등(고)'
# 초등학교 중 유아인 행을 제거
sch_accimdm = sch_accimdm[sch_accimdm['학교급'] != '초등학교']
# '학교급'과 '사고매개물' 컬럼 선택
sch_accimdm = sch_accimdm[['학교급', '사고매개물']]
# 분석 편의를 위해 일부 데이터 값 변경
sch_accimdm['사고매개물'] = sch_accimdm['사고매개물'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()
# 시각화 편의를 위해 중학교, 고등학교 값 변경
sch_accimdm['학교급'] = sch_accimdm['학교급'].replace({'중학교': '중등', '고등학교': '고등'})
# 컬럼명 변경
sch_accimdm.rename(columns={'사고매개물': '사고 매개물'}, inplace=True)

# age_accitime 데이터프레임(5개년 누적)
# '학교급'의 '유치원', '특수학교', '기타학교' 값 제외
age_accitime = df[
    (df['학교급'] != '유치원') &
    (df['학교급'] != '특수학교') &
    (df['학교급'] != '기타학교')
    ]
# '나이'와 '사고시간' 컬럼 선택
age_accitime = age_accitime[['나이', '사고시간']]
# '나이'가 0인 행 추가 제거
age_accitime = age_accitime[age_accitime['나이'] != 0]
# 분석 편의를 위해 일부 데이터 값 변경
age_accitime = age_accitime.replace('점심시간', '식사시간')
age_accitime = age_accitime.replace('석식시간', '식사시간')
age_accitime = age_accitime.replace('휴식시간 및 청소시간', '휴식/청소시간')
# 컬럼명 변경
age_accitime.rename(columns={'사고시간': '사고 시간'}, inplace=True)

# age_acciplace 데이터프레임(5개년 누적)
# '학교급'의 '유치원', '특수학교', '기타학교' 값 제외
age_acciplace = df[
    (df['학교급'] != '유치원') &
    (df['학교급'] != '특수학교') &
    (df['학교급'] != '기타학교')
    ]
# '나이'와 '사고장소' 컬럼 선택
age_acciplace = age_acciplace[['나이', '사고장소']]
# '나이'가 0인 행 추가 제거
age_acciplace = age_acciplace[age_acciplace['나이'] != 0]
# 분석 편의를 위해 일부 데이터 값 변경
age_acciplace = age_acciplace.replace('교외활동', '교외')
# 컬럼명 변경
age_acciplace.rename(columns={'사고장소': '사고 장소'}, inplace=True)

# age_accipart 데이터프레임(5개년 누적)
# '학교급'의 '유치원', '특수학교', '기타학교' 값 제외
age_accipart = df[
    (df['학교급'] != '유치원') &
    (df['학교급'] != '특수학교') &
    (df['학교급'] != '기타학교')
    ]
# '나이'와 '사고부위' 컬럼 선택
age_accipart = age_accipart[['나이', '사고부위']]
# '나이'가 0인 행 추가 제거
age_accipart = age_accipart[age_accipart['나이'] != 0]
# 분석 편의를 위해 일부 데이터 값 변경
age_accipart['사고부위'] = age_accipart['사고부위'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()
# 컬럼명 변경
age_accipart.rename(columns={'사고부위': '사고 부위'}, inplace=True)

# age_accitype 데이터프레임(5개년 누적)
# '학교급'의 '유치원', '특수학교', '기타학교' 값 제외
age_accitype = df[
    (df['학교급'] != '유치원') &
    (df['학교급'] != '특수학교') &
    (df['학교급'] != '기타학교')
    ]
# '나이'와 '사고형태' 컬럼 선택
age_accitype = age_accitype[['나이', '사고형태']]
# '나이'가 0인 행 추가 제거
age_accitype = age_accitype[age_accitype['나이'] != 0]
# 분석 편의를 위해 일부 데이터 값 변경
age_accitype = age_accitype.replace('낙상-미끄러짐', '낙상')
age_accitype = age_accitype.replace('낙상-넘어짐', '낙상')
age_accitype = age_accitype.replace('낙상-떨어짐', '낙상')
age_accitype = age_accitype.replace('염좌·삐임 등 신체 충격', '신체 충격')
# 컬럼명 변경
age_accitype.rename(columns={'사고형태': '사고 형태'}, inplace=True)

# age_acciact 데이터프레임(5개년 누적)
# '학교급'의 '유치원', '특수학교', '기타학교' 값 제외
age_acciact = df[
    (df['학교급'] != '유치원') &
    (df['학교급'] != '특수학교') &
    (df['학교급'] != '기타학교')
    ]
# '나이'와 '사고당시활동' 컬럼 선택
age_acciact = age_acciact[['나이', '사고당시활동']]
# '나이'가 0인 행 추가 제거
age_acciact = age_acciact[age_acciact['나이'] != 0]
# 컬럼명 변경
age_acciact.rename(columns={'사고당시활동': '사고 당시 활동'}, inplace=True)

# age_accimdm 데이터프레임(5개년 누적)
# '학교급'의 '유치원', '특수학교', '기타학교' 값 제외
age_accimdm = df[
    (df['학교급'] != '유치원') &
    (df['학교급'] != '특수학교') &
    (df['학교급'] != '기타학교')
    ]
# '나이'와 '사고매개물' 컬럼 선택
age_accimdm = age_accimdm[['나이', '사고매개물']]
# '나이'가 0인 행 추가 제거
age_accimdm = age_accimdm[age_accimdm['나이'] != 0]
# 분석 편의를 위해 일부 데이터 값 변경
age_accimdm['사고매개물'] = age_accimdm['사고매개물'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()
# 컬럼명 변경
age_accimdm.rename(columns={'사고매개물': '사고 매개물'}, inplace=True)

# 탭별 그래프 추가 함수  
def render_tab(df1, df2, acci_content):
    
    # 레이아웃 지정
    col = st.columns((0.3, 2, 0.3, 4, 0.3), gap='medium')
    
    with col[1]:
        st.markdown('######')
        st.markdown(f'''
            <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
            학교급과 {acci_content}
            </h4>
            ''', unsafe_allow_html=True)
        
        # df1 그래프 시각화
        st.plotly_chart(plot_heatmap(df1, '학교급', acci_content, '빈도수', custom_order))
        
    with col[3]:
        st.markdown('######')
        st.markdown(f'''
            <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
            나이와 {acci_content}
            </h4>
            ''', unsafe_allow_html=True)
        
        # df2 그래프 시각화
        st.plotly_chart(plot_boxplot(df2, acci_content, '나이'))
        
# 각 탭에서의 함수 실행
with tab1:
    render_tab(sch_accitime, age_accitime, '사고 시간')
with tab2:
    render_tab(sch_acciplace, age_acciplace, '사고 장소')
with tab3:
    render_tab(sch_accipart, age_accipart, '사고 부위')
with tab4:
    render_tab(sch_accitype, age_accitype, '사고 형태')
with tab5:
    render_tab(sch_acciact, age_acciact, '사고 당시 활동')
with tab6:
    render_tab(sch_accimdm, age_accimdm, '사고 매개물')
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import matplotlib.pyplot as plt
import json


# chart 생성
def count_to(df):
    series_copy = df.copy()
    series_copy.dropna(inplace=True)
    first_list = series_copy.tolist()

    words_to_split = [word for word in first_list if ',' in str(word)]
    for word in words_to_split:
        first_list.remove(word)
        first_list.extend(word.split(','))

    unique_words = list(set(first_list))
    counts = [first_list.count(word) for word in unique_words]

    count_df = pd.DataFrame({df.name: unique_words, '건수': counts})
    count_df = count_df.sort_values('건수', ascending=False).reset_index(drop=True)

    count_df.reset_index(drop=True, inplace=True)
    per = []

    for i in range(0, len(count_df)):
        per.append(round(count_df['건수'].loc[i] / count_df['건수'].sum() * 100, 2))
    count_df['퍼센트(%)'] = per

    count_df.sort_values(by='퍼센트(%)', ascending=False, inplace=True)
    count_df.reset_index(drop = True, inplace=True)

    return count_df



# bar chart 생성
def create_chart(dfs, theme):
    # 색상 팔레트
    palette = ['#A2C5E2']

    # 그래프 생성
    fig = px.bar(dfs, 
                 x='건수', 
                 y=theme, 
                 color=theme, 
                 orientation='h',
                 color_discrete_sequence=palette,  
                 custom_data=['건수', '퍼센트(%)'])

    # 레이아웃 설정
    fig.update_layout(
                font=dict({'family':'KoPubWorld Dotum',
                        'color':'black'}), 
                hoverlabel=dict(       
                    font_size=15,
                    font_family="KoPubWorld Dotum"
                ),
                paper_bgcolor='white',  
                plot_bgcolor='white',
                margin=dict(t=0, b=10, l=10, r=10),  
                showlegend=False,
                xaxis=dict(title='', showticklabels=False),
                yaxis=dict(title='', showticklabels=True))  
                

    # hover 시 정보 설정
    fig.update_traces(
        hovertemplate='<b><br>%{y}</b></br>%{customdata[0]}건</br>%{customdata[1]}%<br><extra></extra>'
    )

    return st.plotly_chart(fig)


# 지역 chart 생성 - 시도
def region_chart(df, year):
                current_data = df[df['연도'] == year]
                
                for index, row in current_data.iterrows():
                    reion = row['지역']
                    count = row['총사고수']
                    change_rate = row['전년대비증감률']
                    change_color = 'green' if change_rate > 0 else 'grey' if change_rate == 0 else 'red'
                    change_icon = '↑' if change_rate > 0 else '-' if change_rate == 0 else '↓'

                    st.markdown(f"""
                    <div style="display: flex; align-items: center; justify-content: space-between; margin: 0; padding: 0; width: 150px;">
                        <p style="margin: 0; padding: 0; font-size: 15px; font-weight: bold; width: 50px; text-align: left;">{reion}</p>
                        <p style="margin: 0; padding: 0; font-size: 15px; width: 50px; text-align: center;">{count}</p>
                        <p style="margin: 0; padding: 0; color: {change_color}; font-size: 8px; width: 50px; text-align: right;">{change_icon} {abs(change_rate):.2f}%</p>
                    </div>
                    """, unsafe_allow_html=True)


# bar chart 생성 - 교육청
def create_chart_detail(dfs, theme):
    # 색상 팔레트
    palette = ['#A2C5E2']
    
    # 막대 두께 설정 (예: 0.4)
    bar_width = 0.4

    # 데이터 순서를 뒤집기 위해 역순으로 정렬
    dfs = dfs[::-1]

    # 그래프 생성
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dfs['건수'],
        y=dfs[theme],
        orientation='h',
        marker_color=palette[0],
        customdata=dfs[['건수', '퍼센트(%)']],
        width=bar_width  # 막대 두께 고정
    ))

    # 레이아웃 설정
    fig.update_layout(
        font=dict({'family':'KoPubWorld Dotum',
                   'color':'black'}), 
        hoverlabel=dict(
            font_size=15,
            font_family="KoPubWorld Dotum"
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(t=0, b=10, l=10, r=10),
        showlegend=False,
        barmode='stack',  # 막대가 너무 뚱뚱하지 않도록 설정
        xaxis=dict(title='', showticklabels=False),
        yaxis=dict(title='', showticklabels=True)
    )

    # hover 시 정보 설정
    fig.update_traces(
        hovertemplate='<b><br>%{y}</b></br>%{customdata[0]}건</br>%{customdata[1]}%<br><extra></extra>'
    )

    return st.plotly_chart(fig)


# 지역 chart 생성 - 교육청
def region_chart_detail(df):
                for index, row in df.iterrows():
                    reion = row['교육청']
                    count = row['건수']
                    change_rate = row['전년대비증감률']
                    change_color = 'green' if change_rate > 0 else 'grey' if change_rate == 0 else 'red'
                    change_icon = '↑' if change_rate > 0 else '-' if change_rate == 0 else '↓'

                    st.markdown(f"""
                    <div style="display: flex; align-items: center; justify-content: space-between; margin: 0; padding: 0; width: 300px;">
                        <p style="margin: 0; padding: 0; font-size: 15px; font-weight: bold; width: 150px; text-align: left;">{reion}</p>
                        <p style="margin: 0; padding: 0; font-size: 15px; width: 50px; text-align: center;">{count}</p>
                        <p style="margin: 0; padding: 0; color: {change_color}; font-size: 8px; width: 50px; text-align: right;">{change_icon} {abs(change_rate):.2f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
    



# 지역 표기 형식 변경 함수
def extract_region(name):
    if name in ['충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도']:
        return name[:1] + name[2]
    else:
        return name[:2]
    
# 학교별 데이터 전처리 함수 - 시도별
def schooldf1(inputdf):
    df = inputdf.parse('요약정보', skiprows=8)
    df.rename(columns={'행 레이블': '지역', '합계 : 학생수_총계_계':'학생수'}, inplace=True)
    df = df[df['지역'] != '총합계']
    return df
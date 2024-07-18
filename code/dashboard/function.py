## 대시보드에 사용할 함수를 정의

import pandas as pd
import numpy as np
import polars as pl
from datetime import datetime
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 그래프 색
palette = ["#5c7dd2","#92b8ff","#aeceff","#c7e4ff",'#c3b7eb', '#9590e6', '#837ed5']

# 계절별 팔레트 설정
spring = ["#f08080","#f4978e","#f8ad9d","#fbc4ab","#ffdab9"][::-1]
summer = ["#d9ed92", "#b5e48c", "#99d98c", "#76c893", "#52b69a"]
fall = ["#ffd78a", "#fdc77b", "#fbb76b", "#faa75c", "#f8964c", "#f6863d", "#f4762d"][:-2]
winter = ["#d5deef","#b1c9ef","#8aaee0","#628ecb","#597CAD"]
season_color = [spring,summer,fall,winter]
# 계절별 색깔 지정
season_onecolor = [spring[2],summer[1],fall[1],winter[2]]

def get_grouped_count_spot(df,col,year):
    new_df = df.groupby('사고장소').count()[['구분']].reset_index().replace('교외활동','교외')
    new_df = new_df.groupby('사고장소').sum()[['구분']]
    new_df['퍼센트'] = round(new_df/new_df.sum()*100,1)
    new_df.reset_index(inplace=True)
    new_df.columns = [col,'사고건수','퍼센트']
    new_df['연도'] = str(year)
    return new_df



def horizontal_chart_one_year(df,col):
    fig = px.bar(df.sort_values('사고건수'), x="사고건수", y=col,color_discrete_sequence=[palette[0]])
    fig.update_layout(    
                title={
                'text': f"<b>{df['연도'][0]}년 학교 장소별 안전사고 건수</b>",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font':{'size':24,'family':'KoPubWorld돋움체_Pro'}
                },
                font=dict({'family':'KoPubWorld돋움체_Pro',
                        'color':'black'}), #전체 폰트 설정(로컬 폰트 사용 가능)
                hoverlabel=dict(        #호버 박스 폰트 설정
                    # bgcolor="white",
                    font_size=15,
                    font_family="KoPubWorld돋움체_Pro"
                ),
                paper_bgcolor='white',  # 전체 배경색
                plot_bgcolor='white',    # 플롯 배경색
                legend_title_text='  ',
                yaxis_ticksuffix="  ",
                )           
                # barcornerradius=15

    hover_text = '사고장소 : %{y}<br>사고건수 : %{x}건<extra></extra>'
    fig.update_traces(
                hovertemplate=hover_text)

    fig.update_xaxes(title=' ',
                    title_font_family='KoPubWorld돋움체',
                    tickfont=dict(size=14),
                    tickformat="~2s",
                    )

    fig.update_yaxes(title=' ',
                    tickfont=dict(size=17)
                    # title_font_family='KoPubWorld돋움체 Medium',
                    # tickformat="~2s",
                    # tickfont=dict({'size':15,'family':'KoPubWorld돋움체 Medium'})
                    )
    return fig


def acc_spot_5years_chart(df):
    # 5개년 장소 데이터프레임 생성
    acc_spot_5years = df.pivot_table(index='연도', columns='사고장소', values=['사고건수','퍼센트']).reindex(index=['2019','2020','2021','2022','2023'])
    # 각 사고장소 별로 trace 추가
    fig = go.Figure()

    locations = ["교외", "교실", "부속시설", "운동장", "통로"]
    colors = palette

    for location, color in zip(locations, colors):
        fig.add_trace(go.Bar(
            x=acc_spot_5years.index,
            y=acc_spot_5years['퍼센트'][location],
            name=location,
            marker_color=color,
            customdata=acc_spot_5years['사고건수'][location],
            hovertemplate='<b>%{x}</b><br>' +
                        '사고장소 : ' + location + '<br>' +
                        '사고 건수 : %{customdata}건<br>' +
                        '퍼센트 : %{y}<extra></extra>',
        ))

    # 레이아웃 업데이트
    fig.update_layout(
        barmode='stack',
        height=500,
        width=1000,
        font=dict(
            family='KoPubWorld돋움체_Pro',
            color='black'
        ),
        title={
        'text': "<b>5개년 학교 장소별 안전사고 건수</b>",
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font':{'size':24,'family':'KoPubWorld돋움체_Pro'}
        },
        hoverlabel=dict(
            font_size=15,
            font_family="KoPubWorld돋움체_Pro"
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        yaxis=dict(
            ticksuffix="%",
        ),
        legend=dict(
            title_text=' '
        ),
        xaxis=dict(
            title=' ',
            tickfont=dict(size=17)
        )
    )

    # 차트 반환
    return fig


def spot_body_fig(df): 

    spot_list = ['교실','운동장','교외','통로','부속시설']
    fig = make_subplots(rows=1, cols=5,
                        subplot_titles=spot_list,
                        horizontal_spacing=0.05)

    for i in range(0,5):

        fig.add_trace(go.Bar(y=df[df['사고장소']==spot_list[i]]['사고부위'].tail(5),
                            x=df[df['사고장소']==spot_list[i]]['구분'].tail(5),
                            name=spot_list[i],orientation='h',
                            marker=dict(color=palette[i]),
                            hovertemplate=f'<b>{spot_list[i]}</b><br>'
                            '사고부위 : %{y}<br>' +
                            '사고건수 : %{x:.f}건<extra></extra>'),
                            1, i+1)
        


    fig.update_layout(   
                font=dict({'family':'KoPubWorld돋움체_Pro',
                        'color':'black',
                        'size':20}), #전체 폰트 설정(로컬 폰트 사용 가능)
                hoverlabel=dict(        #호버 박스 폰트 설정
                    # bgcolor="white",
                    font_size=15,
                    font_family="KoPubWorld돋움체_Pro"
                ),
                paper_bgcolor='white',  # 전체 배경색
                plot_bgcolor='white',    # 플롯 배경색
                legend_title_text='  ',
                height=350,
                showlegend=False,  # 범례 숨기기
                # colors=palette_purple
                # barcornerradius=15
                )

    fig.update_yaxes(ticksuffix='  ',
                    title_font_family='KoPubWorld돋움체 Medium',
                    tickfont=dict(size=15))    

    fig.update_xaxes(
                    title=' ',
                    title_font_family='KoPubWorld돋움체 Medium',
                    tickfont=dict(size=12),
                    # tickformat=",",
                    )



    return fig

def spot_activity_fig(df):
    spot_list = ['교실','운동장','교외','통로','부속시설']
    fig = make_subplots(rows=1, cols=5,
                        subplot_titles=spot_list,
                        horizontal_spacing=0.07)



    for i in range(0,5):

        fig.add_trace(go.Bar(y=df[df['사고장소']==spot_list[i]]['사고당시활동'].tail(5),
                            x=df[df['사고장소']==spot_list[i]]['구분'].tail(5),
                            name=spot_list[i],orientation='h',
                            marker=dict(color=palette[i]),
                            hovertemplate='사고건수 : %{x:.f}건<br>' +
                            '사고당시활동 : %{y}<br><extra></extra>'),
                            1, i+1)
        

    fig.update_layout(   
                font=dict({'family':'KoPubWorld돋움체_Pro',
                        'color':'black',
                        'size':20}), #전체 폰트 설정(로컬 폰트 사용 가능)
                hoverlabel=dict(        #호버 박스 폰트 설정
                    # bgcolor="white",
                    font_size=15,
                    font_family="KoPubWorld돋움체_Pro"
                ),
                paper_bgcolor='white',  # 전체 배경색
                plot_bgcolor='white',    # 플롯 배경색
                legend_title_text='  ',
                height=350,
                showlegend=False,  # 범례 숨기기
                )

    fig.update_yaxes(ticksuffix='  ',
                    title_font_family='KoPubWorld돋움체 Medium',
                    tickfont=dict(size=15))    

    fig.update_xaxes(
                    title=' ',
                    title_font_family='KoPubWorld돋움체 Medium',
                    tickfont=dict(size=12),
                    # tickformat=",",
                    )


    return fig

def acc_month_fig(df):
    months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
    fig = px.bar(df, x="사고월", y="사고건수",
                height=500,
                width=1200,
                color_discrete_sequence=palette,
                hover_name="사고월",
                category_orders={'사고월': months})  # 원하는 순서로 카테고리 순서 지정)

    fig.update_traces(
                hovertemplate='사고월 : %{x}<br>'+'사고건수 : %{y}건')

    fig.update_layout(
                title={
                'text': "<b>5개년 월별 안전사고 누적 건수 (2019~2023)</b>",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font':{'size':24,'family':'KoPubWorld돋움체_Pro'}
                },
                font=dict({'family':'KoPubWorld돋움체_Pro',
                        'color':'black'}), #전체 폰트 설정(로컬 폰트 사용 가능)
                hoverlabel=dict(        #호버 박스 폰트 설정
                    # bgcolor="white",
                    font_size=15,
                    font_family="KoPubWorld돋움체_Pro"
                ),
                paper_bgcolor='white',  # 전체 배경색
                plot_bgcolor='white',    # 플롯 배경색
                # yaxis_ticksuffix=" ",
                )




    fig.update_xaxes(title=' ',
                    title_font_family='KoPubWorld돋움체 Medium',
                    tickfont=dict(size=17))

    fig.update_yaxes(title=' ',
                    title_font_family='KoPubWorld돋움체 Medium',
                    tickformat="~2s",
                    tickfont=dict({'size':15,'family':'KoPubWorld돋움체 Medium'})
                    )
    return fig


def month_spot_fig(df): # 계절별 사고장소
    # heatmap 그리기 위한 데이터 재구성
    months = df['사고월']
    spots = df['사고장소']
    values = df['사고건수']

    fig = go.Figure(data=go.Heatmap(
        z=values,
        x=months,
        y=spots,
        colorscale=['#e5edfb', '#ccdbf7', '#b2c9f3', '#99b6ef', '#7fa4eb', '#6592e7', '#4c80e3', '#326edf']

    ,  # 색상 스케일 설정
        colorbar=dict(title='사고건수',
                        titlefont=dict(size=12)),  # colorbar 설정
    ))
    fig.update_traces(
                hovertemplate='사고장소 : %{y}'+'<br>사고월 : %{x}'+'<br>사고건수 : %{z:.f}건<extra></extra>')
    fig.update_xaxes(categoryorder='array', categoryarray=['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'])
    fig.update_layout(
                font=dict({'family':'KoPubWorld돋움체_Pro',
                        'color':'black',
                        'size':18}), #전체 폰트 설정(로컬 폰트 사용 가능)
                hoverlabel=dict(        #호버 박스 폰트 설정
                    # bgcolor="white",
                    font_size=15,
                    font_family="KoPubWorld돋움체_Pro"
                ),
                paper_bgcolor='white',  # 전체 배경색
                plot_bgcolor='white',    # 플롯 배경색
                yaxis_ticksuffix=" ",
                yaxis=dict(
                title=' ',
                title_font_family='KoPubWorld돋움체 Medium',
                tickfont=dict(size=15),
            ),
                )


    # 차트 보여주기
    return fig


def  season_body_fig(df): #계절별 사고부위

    # 서브플롯 생성
    fig = make_subplots(rows=1, cols=4, subplot_titles=(['봄', '여름', '가을', '겨울']))

    # 각 계절에 대한 바 차트 추가
    for i, season in enumerate(['봄', '여름', '가을', '겨울']):
        season_data = df[df['계절'] == season]
        fig.add_trace(
            go.Bar(
                y=season_data['사고부위'],
                x=season_data['사고건수'],
                orientation='h',  # 가로 바 차트로 설정
                name=season,
                marker=dict(color=season_onecolor[i])
            ),
            row=1, col=i+1
        )

    # hovertemplate 설정
    fig.update_traces(hovertemplate='<b>%{label}</b><br>사고건수 : %{value:.f%}건')

    # 레이아웃 업데이트
    fig.update_layout(
        # title={
        # 'text': "<b>계절별 안전사고 부위 (2019~2023)</b><br><br>",
        # 'yanchor': 'top',
        # 'font':{'size':24,'family':'KoPubWorld돋움체_Pro'}
        # },
        font=dict(
            family='KoPubWorld돋움체_Pro',
            color='black',
            size=18
        ),
        hoverlabel=dict(
            font_size=15,
            font_family="KoPubWorld돋움체_Pro"
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        legend=dict(
            title_text=' '
        ),
        
    )

    # 서브플롯 각각의 레이아웃 업데이트
    for i, season in enumerate(['봄', '여름', '가을', '겨울']):
        fig.update_xaxes(title=' ', title_font_family='KoPubWorld돋움체 Medium', tickfont=dict(size=12), row=1, col=i+1)
        fig.update_yaxes(title=' ', tickfont=dict(size=15), row=1, col=i+1,ticksuffix=" ")

    # subplot title 크기 조정
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(size=20)  # 원하는 크기로 설정
    # 차트 보여주기
    return fig

# def season_activity_fig(df): # 계절별 사고당시활동
#     # 계절별로 데이터프레임 나누기
#     seasons = df['계절'].unique()

#     # 서브플롯 생성
#     fig = make_subplots(rows=1, cols=4, subplot_titles=seasons, specs=[[{'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}]],
#                         horizontal_spacing=0.05)

#     # 각 계절에 대해 파이 차트 추가
#     for i, season in enumerate(seasons):
#         season_df = df[df['계절'] == season]
#         fig.add_trace(go.Pie(
#             labels=season_df['사고당시활동'],
#             values=season_df['사고건수'],
#             name=season,
#             textinfo='percent+label',
#             marker=dict(colors=['#D4D4DB','#BABAC0',"9F9FA4"]+season_color[i][::-1])
#         ), row=1, col=i+1)

#     # hovertemplate 설정
#     fig.update_traces(hovertemplate='<b>%{label}</b><br>사고건수 : %{value}건<br>퍼센트 : %{percent}%<extra></extra>')


#     # 레이아웃 업데이트
#     fig.update_layout(
#         # title={
#         # 'text': "<b>계절별 사고당시활동 분포 (2019~2023)</b><br><br>",
#         # 'yanchor': 'top',
#         # 'font':{'size':24,'family':'KoPubWorld돋움체_Pro'}
#         # },
#         font=dict(
#             family='KoPubWorld돋움체_Pro',
#             color='black',
#             size=15
#         ),
#         hoverlabel=dict(
#             font_size=15,
#             font_family="KoPubWorld돋움체_Pro"
#         ),
#         paper_bgcolor='white',
#         plot_bgcolor='white',
#         showlegend =False,
#         xaxis=dict(
#             title=' ',
#             title_font_family='KoPubWorld돋움체 Medium',
#             # tickfont=dict(size=15),
#             categoryorder='array',
#             categoryarray=seasons
#         ),
#         margin=dict(l=50,b=120)  # 여백 조정
#     )
#     # 각 서브플롯 제목의 텍스트 크기 업데이트
#     for annotation in fig['layout']['annotations']:
#         annotation['font'] = dict(size=20)  # 원하는 크기로 설정

#     # 차트 보여주기
#     return fig

def season_activity_fig(df): # 계절별 사고당시활동
    # 계절별로 데이터프레임 나누기
    seasons = df['계절'].unique()

    # 서브플롯 생성
    fig = make_subplots(rows=1, cols=4, subplot_titles=seasons, specs=[[{'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}]])


    # 각 계절에 대해 파이 차트 추가
    for i, season in enumerate(seasons):
        season_df = df[df['계절'] == season]
        fig.add_trace(go.Pie(
            labels=season_df['사고당시활동'],
            values=season_df['사고건수'],
            name=season,
            textinfo='percent+label',
            marker=dict(colors=['#D4D4DB','#BABAC0',"9F9FA4"]+season_color[i][::-1])
        ), row=1, col=i+1)

    # hovertemplate 설정
    fig.update_traces(hovertemplate='<b>%{label}</b><br>사고건수: %{value}건<br>퍼센트: %{percent}<extra></extra>')


    # 레이아웃 업데이트
    fig.update_layout(
        font=dict(
            family='KoPubWorld돋움체_Pro',
            color='black',
        ),
        hoverlabel=dict(
            font_size=15,
            font_family="KoPubWorld돋움체_Pro"
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=False,
    )

    # 각 서브플롯 제목의 텍스트 크기 업데이트
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(size=20)  # 원하는 크기로 설정

    # 차트 보여주기
    return fig


## 안전 사고 발생 사고시간 Top 5
def acc_time_top5_fig(df):
    fig = px.bar(df.tail(5), x="사고건수", y='사고시간',color_discrete_sequence=[palette[0]])
    fig.update_layout(    
                font=dict({'family':'KoPubWorld돋움체_Pro',
                        'color':'black'}), #전체 폰트 설정(로컬 폰트 사용 가능)
                hoverlabel=dict(        #호버 박스 폰트 설정
                    # bgcolor="white",
                    font_size=15,
                    font_family="KoPubWorld돋움체_Pro"
                ),
                paper_bgcolor='white',  # 전체 배경색
                plot_bgcolor='white',    # 플롯 배경색
                legend_title_text='  ',
                yaxis_ticksuffix="  ",
                
                # barcornerradius=15
                )
    # hovertemplate 설정
    fig.update_traces(hovertemplate='사고시간 : %{y}<br>사고건수 : %{x}건<extra></extra>')

    fig.update_xaxes(title=' ',
                    title_font_family='KoPubWorld돋움체 Medium',
                    tickfont=dict(size=14),
                    tickformat="~2s",
                    )

    fig.update_yaxes(title=' ',
                    tickfont=dict(size=17)
                    )
    return fig

def time_tree_map(df):
    # Treemap 생성
    fig = px.treemap(
        df,
        path=['사고시간', '사고당시활동'],  # Treemap의 경로 (계층 구조)
        values='구분',  # 크기 값
        color_discrete_sequence=palette
    )

    # 텍스트 크기를 크게 조정
    # fig.update_traces(textinfo="label+value+percent entry", textfont_size=16)
    fig.update_traces(textinfo="label+value", textfont_size=17,    
                    hoverinfo='none',  # Hover 정보를 숨김 
                    hovertemplate=None  # Hover 템플릿을 비활성화
                    )
    fig.update_layout(   
                font=dict({'family':'KoPubWorld돋움체_Pro',
                        'color':'black',
                        'size':20}), #전체 폰트 설정(로컬 폰트 사용 가능)
                # hoverlabel=dict(        #호버 박스 폰트 설정
                #     # bgcolor="white",
                #     font_size=15,
                #     font_family="KoPubWorld돋움체_Pro"
                # ),
                paper_bgcolor='white',  # 전체 배경색
                plot_bgcolor='white',    # 플롯 배경색
                legend_title_text='  ',
                height=500,
                showlegend=False,  # 범례 숨기기
                )

    # Treemap 시각화
    return fig



# 대시보드에 사용할 함수를 정의

import pandas as pd
import numpy as np
import polars as pl
from datetime import datetime
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# 학교급별 시각화 함수

# 하루 평균 발생 안전사고 수 시각화
def sch_aver_acci_chart(df, year):
    current_data = df[df['연도'] == year]
    
    st.markdown('######') 
    st.markdown(f'''
    <h4 style="font-family: 'KoPubWorld Dotum', sans-serif; margin: 0; padding: 0;">
    하루 평균 발생<br> 안전사고 수
    </h4>
    ''', unsafe_allow_html=True)
    
    st.markdown('######') 
    for index, row in current_data.iterrows():
        school_level = row['학교급']
        average_accidents = row['하루평균사고수']
        change_rate = row['전년대비증감률']
        change_color = 'green' if change_rate > 0 else 'red'
        change_icon = '↑' if change_rate > 0 else '↓'

        st.markdown(f"""
        <div style="margin: 0; padding: 0;">
            <p style="margin: 0 0 10px 0; padding: 0; font-size: 16px; font-weight: bold;">{school_level}</p>
            <h3 style="margin: 0 0 10px 0; padding: 0; font-size: 25px;">{average_accidents}건</h3>
            <p style="margin: 0 0 30px 0; padding: 0; color: {change_color}; font-size: 16px;">{change_icon} {abs(change_rate):.2f}%</p>
        </div>
        """, unsafe_allow_html=True)

# 초등학교 저학년/고학년 구분        
def update_school_level(row):
    if row['학교급'] == '초등학교':
        if row['사고자학년'] == '1학년' or row['사고자학년'] == '2학년' or row['사고자학년'] == '3학년':
            return '초등학교_저학년'
        elif row['사고자학년'] == '4학년' or row['사고자학년'] == '5학년' or row['사고자학년'] == '6학년':
            return '초등학교_고학년'
        
    return row['학교급']

# 학교급별 총 사고 수 시각화(1)
def create_h_barchart(df, year, x_col, y_col, y_order):
    year_df = df[df['연도'] == year]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=year_df[y_col],
        x=year_df[x_col],
        orientation='h',
        marker=dict(color='#4a5fa8'),
        hovertemplate=f'<b>%{{y}}</b><br>사고수: %{{x:,}}건<extra></extra>'
        ))
    fig.update_layout(
        font=dict(
            family='KoPubWorld Dotum',
            ),
        hoverlabel=dict(
            font_size=14,
            font_family="KoPubWorld Dotum"
            ),
        yaxis=dict(
            categoryorder='array', 
            categoryarray=y_order
            ),
        height=400,
        width=800,
        margin=dict(t=50)
        )

    return fig

# 학교급별 총 사고 수 시각화(2)
def create_piechart(df, year, name_col, value_col, name_order, colors):
    year_df = df[df['연도'] == year]
    
    fig = px.pie(
        year_df,
        names=name_col,
        values=value_col,
        category_orders={name_col: name_order},
        color=name_col,
        color_discrete_map=colors
        )
    fig.update_traces(texttemplate='%{label}<br><span style="font-size:15px">%{percent:.2%}</span>',
                      hovertemplate='<b>%{label}</b><br>사고수: %{value}건<br>')
    fig.update_layout(
        font=dict(
            family='KoPubWorld Dotum',
            ),
        hoverlabel=dict(
            font_size=14,
            font_family="KoPubWorld Dotum"
            ),
        showlegend=False,
        height=400,
        width=400,
        margin=dict(t=120, r=60)
        )
    
    return fig

# 학교급별 사고자 성별 시각화
def create_pyramid_chart(df, year, x_col, y_col):
    year_df = df[df['연도'] == year]
    male_df = year_df[year_df['사고자성별'] == '남']
    female_df = year_df[year_df['사고자성별'] == '여']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=-male_df[x_col],
        y=male_df[y_col],
        orientation='h',
        name='남',
        customdata=male_df[[x_col, '사고수 비율']],
        marker_color='#c7e4ff',
        text=male_df['사고수 비율'].apply(lambda x: f"{x:.2f}%"),
        textposition='inside',
        texttemplate='%{text}'
        ))
    fig.add_trace(go.Bar(
        x=female_df[x_col],
        y=female_df[y_col],
        orientation='h',
        name='여',
        customdata=female_df[[x_col, '사고수 비율']],
        marker_color='#FFE0B2',
        text=female_df['사고수 비율'].apply(lambda x: f"{x:.2f}%"),
        textposition='inside',
        texttemplate='%{text}'
        ))
    fig.update_layout(
        barmode='relative',
        bargap=0.01,
        legend_orientation='h',
        legend_x=1,
        legend_y=1.24,
        legend_xanchor='right',
        legend_yanchor='top',
        font=dict(
            family='KoPubWorld Dotum',
            color='black'
            ),
        hoverlabel=dict(
            font_size=14,
            font_family="KoPubWorld Dotum"
            ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        legend_title_text=' ',
        height=430,
        width=800,
        margin=dict(t=85, r=30)
        )

    hover_text_male = '<b>%{y}</b><br>사고수: %{customdata[0]:.f}건<br>퍼센트: %{customdata[1]:.2f}%'
    hover_text_female = '<b>%{y}</b><br>사고수: %{customdata[0]:.f}건<br>퍼센트: %{customdata[1]:.2f}%'

    fig.update_traces(
        hovertemplate=hover_text_male,
        selector=dict(name='남')
        )
    fig.update_traces(
        hovertemplate=hover_text_female,
        selector=dict(name='여')
        )
    fig.update_xaxes(
        showticklabels=True,
        title_text="",
        title_font=dict(size=12)  
        )
    fig.update_yaxes(
        tickfont=dict(size=12)  
        )

    return fig

# 학교급별 사고자 학년 시각화
def create_donut_chart(df, year, sch_level, name_col, value_col, name_order, colors):
    sch_year_df = df[(df['연도'] == year) & (df['학교급'] == sch_level)]
    
    fig = px.pie(
        sch_year_df,
        names=name_col,
        values=value_col,
        hole=0.4,
        category_orders={name_col: name_order},
        color=name_col,
        color_discrete_map=colors,
        )
    fig.update_layout(
        annotations=[
            dict(
                text=sch_level,
                x=0.5,
                y=0.5,
                font_size=15,
                showarrow=False
                )
            ]
        )
    fig.update_traces(texttemplate='%{label}<br><span style="font-size:13px">%{percent:.2%}</span>',
                      hovertemplate='<b>%{label}</b><br>사고수: %{value:,}건<br>')
    fig.update_layout(
        font=dict(
            family='KoPubWorld Dotum',
            color='black'
            ),
        hoverlabel=dict(
            font_size=14,
            font_family="KoPubWorld Dotum"
            ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=False,
        height=360,
        width=360,
        margin=dict(t=60)
        )

    return fig
    
# 학교급별 사고 수 월별 비교 시각화
def create_stacked_barchart(df, school_type_categories, palette, months):
    fig = go.Figure()
    for category, color in zip(school_type_categories, palette):
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['퍼센트'][category],
            name=category,
            marker_color=color,
            customdata=df['구분'][category],
            hovertemplate='<b>%{x}</b><br>' +
                          '학교급: ' + category + '<br>' +
                          '사고수: %{customdata}건<br>' +
                          '퍼센트: %{y:.2f}%<extra></extra>'
                          ))
    fig.update_layout(
        barmode='stack',
        height=500,
        width=1100,
        font=dict(
            family='KoPubWorld Dotum',
            color='black'
            ),
        hoverlabel=dict(
            font_size=14,
            font_family="KoPubWorld Dotum"
            ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        yaxis=dict(
            ticksuffix="%", title=' '
            ),
        legend=dict(
            title_text=' '
            ),
        xaxis=dict(
            title=' ',
            title_font_family='KoPubWorld Dotum',
            tickfont=dict(size=17),
            categoryorder='array',
            categoryarray=months
            ),
        margin=dict(t=30)
        )

    return fig

def create_sub_barchart(df, category_col, value_col, colors):
    df = df[df['학교급'].notna()]
    unique_school_levels = df['학교급'].unique()
    
    num_rows = 2
    num_cols = 3
    fig = make_subplots(
        rows=num_rows, cols=num_cols,  
        subplot_titles=unique_school_levels,  
        horizontal_spacing=0.15,
        vertical_spacing=0.3
        )
    for i, school_level in enumerate(unique_school_levels):
        row = i // num_cols + 1
        col = i % num_cols + 1
        level_data = df[df['학교급'] == school_level].sort_values(value_col, ascending=False).head(5)
        fig.add_trace(
            go.Bar(
                y=level_data[category_col],
                x=level_data[value_col],
                name=school_level,
                orientation='h',
                marker=dict(color=colors.get(school_level)),  
                hovertemplate='<b>%{y}</b><br>사고수: %{x:,}건<extra></extra>',   
                width=0.8
                ),
            row=row, col=col
            )
    fig.update_layout(
        barmode='stack',
        font=dict(
            family='KoPubWorld Dotum',
            color='black',
            size=20
            ),
        hoverlabel=dict(
            font_size=14,
            font_family="KoPubWorld Dotum"
            ),
        height=600,  
        width=1200,  
        showlegend=False,
        margin=dict(t=100)
        )
    fig.update_yaxes(
        autorange="reversed",
        ticksuffix='  ',
        title_font_family='KoPubWorld Dotum',
        tickfont=dict(size=14)
        )   
    fig.update_xaxes(
        title=' ',
        title_font_family='KoPubWorld Dotum',
        tickfont=dict(size=14)
        )
    
    return fig
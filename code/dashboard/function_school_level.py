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
import streamlit as st

# 학교급별 시각화 함수

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
        
def update_school_level(row):
    if row['학교급'] == '초등학교':
        if row['사고자학년'] == '1학년' or row['사고자학년'] == '2학년' or row['사고자학년'] == '3학년':
            return '초등학교_저학년'
        elif row['사고자학년'] == '4학년' or row['사고자학년'] == '5학년' or row['사고자학년'] == '6학년':
            return '초등학교_고학년'
    return row['학교급']

def create_piechart(df, year, name_col, value_col, name_order, colors):
    year_df = df[df['연도'] == year]
    fig = px.pie(
        year_df,
        names=name_col,
        values=value_col,
        category_orders={name_col: name_order},
        color=name_col,
        color_discrete_map=colors,
        title=f"{year}년 {name_col}별 {value_col}"
        )
    
    fig.update_traces(texttemplate='<b><span style="font-size:15px">%{percent:.2%}</span></b>',
                      hovertemplate='<b>%{label}</b><br>사고수: %{value}<br>')
    
    fig.update_layout(
        title_text=f'<b><span style="font-size:20x">{year}년 {name_col}별 {value_col}</span></b>',  # Bold and increase font size for title
        title_font=dict(size=20, family='KoPubWorld돋움체_Pro'),
        margin=dict(t=105)
        )

    return fig

def create_pyramid_chart(df, year):
    year_df = df[df['연도'] == year]
    male_df = year_df[year_df['사고자성별'] == '남']
    female_df = year_df[year_df['사고자성별'] == '여']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=-male_df['사고수'],
        y=male_df['학교급'],
        orientation='h',
        name='남',
        customdata=male_df[['사고수', '사고수 비율']],
        marker_color='#c7e4ff',
        text=male_df['사고수 비율'].apply(lambda x: f"<b>{x:.2f}%</b>"),
        textposition='inside',
        texttemplate='%{text}'
    ))
    fig.add_trace(go.Bar(
        x=female_df['사고수'],
        y=female_df['학교급'],
        orientation='h',
        name='여',
        customdata=female_df[['사고수', '사고수 비율']],
        marker_color='#FFE0B2',
        text=female_df['사고수 비율'].apply(lambda x: f"<b>{x:.2f}%</b>"),
        textposition='inside',
        texttemplate='%{text}'
    ))

    fig.update_layout(
        barmode='relative',
        bargap=0.01,
        legend_orientation='h',
        legend_x=0.05,
        legend_y=1.2,
        title={
            'text': f"<b>{year}년 학교급별 사고 건수 성별 분포</b>",
            'yanchor': 'top',
            'font': {'size': 20, 'family': 'KoPubWorld돋움체_Pro'}
        },
        font=dict(
            family='KoPubWorld돋움체_Pro',
            color='black'
        ),
        hoverlabel=dict(
            font_size=15,
            font_family="KoPubWorld돋움체_Pro"
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        legend_title_text=' ',
        margin=dict(t=100)
    )

    hover_text_male = '학교급 : %{y}<br>사고건수 : %{customdata[0]:.f}건<br>사고수 비율 : %{customdata[1]:.2f}%'
    hover_text_female = '학교급 : %{y}<br>사고건수 : %{customdata[0]:.f}건<br>사고수 비율 : %{customdata[1]:.2f}%'

    fig.update_traces(
        hovertemplate=hover_text_male,
        selector=dict(name='남')
    )
    fig.update_traces(
        hovertemplate=hover_text_female,
        selector=dict(name='여')
    )

    fig.update_xaxes(showticklabels=True, title_text="사고수")
    fig.update_yaxes(tickfont=dict(size=13))

    return fig

def create_donut_chart(df, school_level, year):
    year_df = df[df['연도'] == year]
    school_df = year_df[year_df['학교급'] == school_level]
    
    if school_df.empty:
        return go.Figure()
    
    # Calculate total and percentage
    total_accidents = school_df['사고수'].sum()
    school_df['사고수 비율'] = (school_df['사고수'] / total_accidents) * 100
    
    fig = go.Figure(data=[go.Pie(
        labels=school_df['사고자성별'],
        values=school_df['사고수 비율'],
        hole=0.4,
        textinfo='label+percent',
        textfont=dict(size=14, family='KoPubWorld돋움체_Pro'),
        marker=dict(colors=['#c7e4ff', '#FFE0B2'])
    )])
    
    fig.update_layout(
        title={
            'text': f"{school_level}의 사고 비율 ({year})",
            'font': {'size': 18, 'family': 'KoPubWorld돋움체_Pro'}
        },
        font=dict(
            family='KoPubWorld돋움체_Pro',
            color='black'
        ),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    return fig

def get_season(date):
            month = date.month
            if month in [3, 4, 5]:
                return '봄'
            elif month in [6, 7, 8]:
                return '여름'
            elif month in [9, 10, 11]:
                return '가을'
            else:
                return '겨울'
    
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
                          '학교급 : ' + category + '<br>' +
                          '사고 건수 : %{customdata}건<br>' +
                          '퍼센트 : %{y}<extra></extra>',
        ))

    fig.update_layout(
        barmode='stack',
        height=500,
        width=1000,
        font=dict(
            family='KoPubWorld돋움체_Pro',
            color='black'
        ),
        hoverlabel=dict(
            font_size=15,
            font_family="KoPubWorld돋움체_Pro"
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
            title_font_family='KoPubWorld돋움체 Medium',
            tickfont=dict(size=17),
            categoryorder='array',
            categoryarray=months
        ),
    )

    return fig

def create_barchart(df, category_column, value_column, title):
    fig = make_subplots(
        rows=1, cols=6, 
        subplot_titles=["초등학교", "중학교", "고등학교"], 
        horizontal_spacing=0.05
    )

    for i, school_level in enumerate(df['학교급'].unique(), start=1):
        level_data = df[df['학교급'] == school_level].sort_values(value_column, ascending=False).head(5)
        fig.add_trace(
            go.Bar(y=level_data[category_column], x=level_data[value_column], name=school_level, orientation='h', marker=dict(color='#aeceff'),
                   hovertemplate='<b>%{y}</b><br>사고수: %{x:,}<extra></extra>'),
            row=1, col=i
        )

    fig.update_layout(title_text=title, barmode='stack', height=600, width=1800)
    
    return fig
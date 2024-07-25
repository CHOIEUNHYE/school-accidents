# 대시보드에 사용할 함수를 정의

import plotly.express as px
import plotly.graph_objects as go

# 추가 분석 시각화 함수

# '사고자학년'에 접두사(학교급) 추가 함수
def add_prefix(row):
    if row['학교급'] == '초등학교':
        return f'초등_{row["사고자학년"]}'
    elif row['학교급'] == '중학교':
        return f'중등_{row["사고자학년"]}'
    elif row['학교급'] == '고등학교':
        return f'고등_{row["사고자학년"]}'
    else:
        return row['사고자학년']

# 학교급과 사고 수 간의 관계 분석 시각화
def create_h_barchart(df, x_col, y_col, y_order):

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df[y_col],
        x=df[x_col],
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

# 나이와 사고 수 간의 관계 분석 시각화
def create_line_chart(df, x_col, y_col):
    corr = df[[x_col, y_col]].corr().iloc[0, 1]
    
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        labels={x_col: x_col, y_col: y_col},
        markers=True
        )
    fig.update_layout(
        font=dict(
            family='KoPubWorld Dotum',
            ),
        hoverlabel=dict(
            font_size=14,
            font_family="KoPubWorld Dotum"
            ),
        height=400,
        width=800,
        margin=dict(t=50)
        )
    fig.update_traces(
        line=dict(color='#4a5fa8'), 
        marker=dict(
            color='#4a5fa8',
            size=8
            ),
        hovertemplate=f'<b>%{{x}}살</b><br>사고수: %{{y:,}}건<extra></extra>'
        )
    fig.add_annotation(
        xref="paper", 
        yref="paper",
        x=1, 
        y=0.95,
        xanchor='right', 
        yanchor='top',
        text=f"상관 계수: {corr:.2f}",
        showarrow=False,
        font=dict(
            size=14, 
            family='KoPubWorld Dotum'
            ),
        bgcolor='#FFFFFF'
        )
    fig.update_xaxes(title='')
    fig.update_yaxes(title='')
    
    return fig

# 학교급과 사고 내용 간의 관계 분석 시각화
def plot_heatmap(df, x_col, y_col, value_col, x_order):
    heatmap_data = df.groupby([x_col, y_col]).size().reset_index(name=value_col)
    heatmap_data_pivot = heatmap_data.pivot(index=y_col, columns=x_col, values=value_col)
    heatmap_data_pivot = heatmap_data_pivot.reindex(columns=x_order)
    
    fig = px.imshow(
        heatmap_data_pivot,
        text_auto=True, 
        color_continuous_scale='Blues'
        )
    fig.update_layout(
        xaxis=dict(tickmode='linear'),
        yaxis=dict(tickmode='linear'),
        coloraxis_colorbar=dict(title=''),
        font=dict(
            family='KoPubWorld Dotum'
            ),
        hoverlabel=dict(
            font_size=14,
            font_family="KoPubWorld Dotum"
            ),
        height=600,
        width=800,
        margin=dict(t=50)
        )
    fig.update_traces(
        texttemplate= '%{z:,}',
        hovertemplate=f'<b>x: %{{x}}</b><br><b>y: %{{y}}</b><br>값: %{{z:,}}<extra></extra>'
        )
    fig.update_xaxes(title='', tickangle=0)
    fig.update_yaxes(title='')
    fig.update_layout(coloraxis_showscale=False)
    
    return fig

# 나이와 사고 내용 간의 관계 분석 시각화
def plot_boxplot(df, x_col, y_col):
    sort_xlabels = sorted(df[x_col].unique())
    fig = px.box(
        df,
        x=x_col,
        y=y_col,
        labels={x_col: x_col, y_col: y_col},
        category_orders={x_col: sort_xlabels}
        )
    fig.update_traces(
        marker=dict(color='#4a5fa8'),  
        line=dict(color='#4a5fa8', width=2)  
        )
    fig.update_layout(
        font=dict(
            family='KoPubWorld Dotum'
            ),
        hoverlabel=dict(
            font_size=14,
            font_family="KoPubWorld Dotum"
            ),
        height=600,
        width=1100,
        margin=dict(t=50)
        )
    fig.update_xaxes(title='', tickangle=0)
    fig.update_yaxes(title='')
    
    return fig
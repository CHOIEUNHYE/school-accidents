## 대시보드에 사용할 함수를 정의

import pandas as pd
import plotly.express as px


def get_grouped_count(df,col,year):
    new_df = df.groupby(col).count()[['구분']]
    new_df['퍼센트'] = round(new_df/new_df.sum()*100,2)
    new_df['퍼센트'] = new_df['퍼센트'].map(lambda x : str(x)+'%')
    new_df.reset_index(inplace=True)
    new_df.columns = [col,'사고건수','퍼센트']
    new_df['연도'] = str(year)
    new_df[['연도','사고장소']]
    return new_df

def make_px_chart(df,palette = ["#231942","#5e548e","#9f86c0","#be95c4","#e0b1cb"]):
    fig = px.histogram(df, x=df.columns[0], y=df.columns[1],
             color='연도', barmode='group',
             height=400,
             width=1200,
             color_discrete_sequence=palette,
             hover_name="연도")

    hover_text = df.columns[0] + ': %{x}<br>' + df.columns[1] + ': %{y}건'
    fig.update_traces(
                hovertemplate=hover_text)

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
                # yaxis_ticksuffix=" ",
                )


    # legend bold처리
    # fig.for_each_trace(lambda t: t.update(name = '<b>' + t.name +'</b>'))

    fig.update_xaxes(title=' ',
                    title_font_family='KoPubWorld돋움체 Medium',
                    tickfont=dict(size=17))

    fig.update_yaxes(title=' ',
                    title_font_family='KoPubWorld돋움체 Medium',
                    tickformat="~2s",
                    tickfont=dict({'size':15,'family':'KoPubWorld돋움체 Medium'})
                    )
    return fig


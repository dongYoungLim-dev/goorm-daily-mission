"""
1. 미션 내용
- Plotly xaxes, yaxes

2. 해당 미션을 통해 학습 문제 2문제 (임의로 작성)
- Q1) `update_xaxes()`/`update_yaxes()`로 tick 설정(tickangle, tickformat, tickmode)을 바꾸는 방법을 정리해보세요.
- Q2) 2개의 y축(secondary y-axis)이 필요한 예시를 하나 만들고, 왜 단일 y축으로는 해석이 어려운지 설명해보세요.

3. keggle 데이터 링크
- https://www.kaggle.com/datasets/mirichoi0218/insurance
"""

import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

df_insurance = pd.read_csv('/Users/dymacpro/myProject/myDev/My/goorm-ai-study/260131_plotly/data/mission_03_insurance/insurance.csv')
print(df_insurance.head())



def main() -> None:
    # TODO: (예: insurance 데이터) age를 x축, charges를 y축으로 산점도를 만든 뒤
    # x/y 축 제목, 범위, grid, tickformat 등을 조절해보기
    fig = go.Figure(
        data=[
            go.Scatter(
                x=df_insurance['age'],
                y=df_insurance['charges'],
                mode="markers",
                name="charges",
                marker=dict(size=20, color='red', opacity=0.5)
            )
        ]
    )

    fig.update_layout(
      title="Mission 03: Axes (xaxes, yaxes)",
      xaxis = dict(
        title_text="Age", 
        showgrid=True, 
        gridcolor="rgba(0,0,0,0.3)", 
        showline=True, 
        linewidth=2, 
        linecolor='black',
        minor_showgrid=True,
        minor_gridcolor="rgba(0,0,0,0.1)",
        ticks='outside',
        dtick=5,       
      ),
      yaxis = dict(
        title_text="Charges", 
        showgrid=True, 
        gridcolor="rgba(0,0,0,0.3)", 
        showline=True, 
        linewidth=2, 
        linecolor='black',
        minor_showgrid=True,
        minor_gridcolor="rgba(0,0,0,0.1)",
        ticks='inside',
        dtick=5000,
      ),
    )
   

    fig.show()

    '''
    이중 y축을 사용하는 예시를 만들고, 이를 설명한다.
    두개의 다른 데이터를 한개의 Figure에 같이 그리면 축의 범위가 너무 넒어져 아래의 빨간색 라인처럼 각 데이터의 경향 파악이 힘들수 있습니다.
    이때 이중 y축을 사용하여 두개의 데이터를 각각 그리게 되면 데이터의 경향을 더 잘 파악할 수 있습니다.
    '''

    # 왼쪽 y축(Primary)
    fig_secondary_2 = go.Figure(
        go.Scatter(x=[1, 2, 3], y=[40, 50, 60], name="left-axis"),
    )

    # 오른쪽 y축(Secondary)
    fig_secondary_2.add_trace(
        go.Scatter(x=[2, 3, 4], y=[4, 5, 6], name="right-axis"),
    )

    fig_secondary_2.show()

    # Secondary y-axis 예시 (왼쪽 y축 / 오른쪽 y축)
    # IMPORTANT: secondary_y는 go.Figure()가 아니라 make_subplots에서 활성화해야 적용됩니다.
    fig_secondary = make_subplots(specs=[[{"secondary_y": True}]])

    # 왼쪽 y축(Primary)
    fig_secondary.add_trace(
        go.Scatter(x=[1, 2, 3], y=[40, 50, 60], name="left-axis"),
        secondary_y=False,
    )

    # 오른쪽 y축(Secondary)
    fig_secondary.add_trace(
        go.Scatter(x=[2, 3, 4], y=[4, 5, 6], name="right-axis"),
        secondary_y=True,
    )

    fig_secondary.update_layout(title="Mission 03: Secondary Y-Axis Example", xaxis_title="x")
    fig_secondary.update_yaxes(title_text="Left Y", secondary_y=False)
    fig_secondary.update_yaxes(title_text="Right Y", secondary_y=True)
    fig_secondary.show()



if __name__ == "__main__":
    main()


"""
1. 미션 내용
- Plotly 그래프 생성

2. 해당 미션을 통해 학습 문제 2문제 (임의로 작성)
- Q1) `go.Bar`, `go.Scatter`, `go.Histogram`의 차이를 설명하고, 각각 어떤 상황에서 쓰는지 예시를 들어보세요.
- Q2) `fig.update_layout()`로 title, legend, margin을 설정하는 방법을 정리하고 직접 적용해보세요.

3. keggle 데이터 링크
- https://www.kaggle.com/datasets/uciml/iris
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def main() -> None:
    # TODO: Kaggle 데이터(iris)를 pandas로 로드한 뒤,
    # - 종(species)별 sepal_length 평균을 막대그래프로 만들기
    # - 혹은 sepal_length vs sepal_width 산점도 만들기
    df_iris = pd.read_csv('/Users/dymacpro/myProject/myDev/My/goorm-ai-study/260131_plotly/data/mission_01_iris/iris.csv')
    fig_subplots = make_subplots(rows=1, cols=3, subplot_titles=["Iris Bar", "Iris Scatter", "Iris Histogram"])
    sepal_length_mean = df_iris.groupby('Species')['SepalLengthCm'].mean()

    # bar 추가
    # - 종(species)별 sepal_length 평균을 막대그래프로 만들었고, bar 그래프는 각 값의 크기를 직관적으로 비교하기에 효과적이다.
    fig_subplots.add_trace(
      go.Bar(name="iris_bar", x=df_iris['Species'].unique(), y=sepal_length_mean), row=1, col=1
    )
    # scatter 추가
    # - 꽃받침 길이(sepal_length)와 꽃받침 너비(sepal_width) 산점도를 만들었고, scatter 그래프는 두 변수 간의 관계를 시각화하기에 효과적이다.
    fig_subplots.add_trace(
      go.Scatter(name="iris_scatter", x=df_iris['SepalLengthCm'], y=df_iris['SepalWidthCm'], mode='markers', marker=dict(size=20, color='red', opacity=0.5)), row=1, col=2
    )
    # histogram 추가
    # - 꽃받침 길이(sepal_length)와 꽃받침 너비(sepal_width) 히스토그램을 만들었고, histogram 그래프는 데이터의 분포를 시각화하기에 효과적이다.
    fig_subplots.add_trace(
      go.Histogram(name="sepal_length_histogram", x=df_iris['SepalLengthCm'], nbinsx=10), row=1, col=3
    )
    fig_subplots.add_trace(
      go.Histogram(name="sepal_width_histogram", x=df_iris['SepalWidthCm'], nbinsx=10), row=1, col=3
    )
    fig_subplots.add_trace(
      go.Histogram(name="petal_length_histogram", x=df_iris['PetalLengthCm'], nbinsx=10), row=1, col=3
    )
    fig_subplots.add_trace(
      go.Histogram(name="petal_width_histogram", x=df_iris['PetalWidthCm'], nbinsx=10), row=1, col=3
    )


    fig_subplots.update_layout(
      title="Mission 01: Plotly Graph Creation",
      title_x=0,
      title_y=0.98,
      # title_x, title_y: (0,0) ~ (1,1), 꼭지점 기준 왼쪽 상단에서 부터 시계방향으로 각각 (0,1), (1,1), (1,0), (0,0)
      title_font=dict(size=20, color='black'),
      title_font_family="Arial",
      title_font_color="red",
      title_font_size=20,
      #orientation: 범례의 방향 h: 가로, v: 세로
      #yanchor: 범례의 y축 위치 top: 위, bottom: 아래
      #y, x:  범례의 y축 위치 (x, y), 꼭지점 기준 왼쪽 상단에서 부터 시계방향으로 각각 (0,1), (1,1), (1,0), (0,0)
      #xanchor: 범례의 x축 위치 right: 오른쪽, left: 왼쪽
      legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1),
      margin=dict(l=50, r=50, t=100, b=100), #left, right, top, bottom
    )
    fig_subplots.show()


if __name__ == "__main__":
    main()


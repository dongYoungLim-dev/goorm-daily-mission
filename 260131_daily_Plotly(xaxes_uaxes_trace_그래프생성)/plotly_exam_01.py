# graph_objects 패키지를  go 로 불러옴
import plotly.graph_objects as go

# go.Figure() 함수를 활용하여 기본 그래프를 생성
fig = go.Figure(
    # Data 입력
    data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])],
    # layout 입력
    layout=go.Layout(
        title=go.layout.Title(text="A Figure Specified By A Graph Object")
    )
)
#show하면 내 노트북 (주피터 노트북 등)에 그래프가 나타남.
fig.show()


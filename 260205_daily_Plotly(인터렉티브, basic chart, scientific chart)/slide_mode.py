import plotly.express as px 
import pandas as pd
import plotly.graph_objects as go


df = px.data.gapminder()
fig = px.scatter(data_frame=df, x="gdpPercap", y="lifeExp", size="pop", color="continent", log_x=True ,size_max=55 ,range_x=[100,1000], range_y=[25, 90], animation_frame="year")

# log 스케일 : 비율로 

# fig["layout"].pop("updatemenus")
fig.layout.pop("updatemenus") # fig 객체 내부의 layout 객체 중 "updatemenus" 키를 삭제
fig.show()

df2 = px.data.tips()

fig2 = px.scatter(data_frame=df2, x='total_bill', y='tip', color='sex', size='size')
fig2.update_layout(xaxis=dict(rangeslider_visible=True))
fig2.show()

fig3 = go.Figure()

fig3.add_trace(go.Scatter(
  x=[1, 2, 3],
  y=[1, 3, 1]
))

# fig3.show(config=dict(displayModeBar=False)) # 모드바 숨기기
fig3.show(config=dict(
  displayModeBar=True,
  modeBarButtonsToRemove=['zoom', 'pan']
))
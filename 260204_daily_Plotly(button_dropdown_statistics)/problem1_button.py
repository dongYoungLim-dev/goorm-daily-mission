"""
문제 1: Plotly 인터렉티브 버튼 (Button)

목표: 버튼을 클릭하여 차트 타입을 변경할 수 있는 인터렉티브 차트 만들기
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ============================================================================
# 데이터 준비
# ============================================================================
# Region별 Sales 합계 데이터
# 이 데이터를 사용하는 이유:
# - Region은 4개의 카테고리(Central, East, South, West)로 구성되어 있어
#   막대/선/파이 차트로 전환할 때 시각적으로 비교하기 좋습니다
# - 각 Region의 Sales 합계가 명확하게 구분되어 있어 버튼으로 차트 타입을
#   전환해도 데이터의 의미를 쉽게 파악할 수 있습니다
region_sales = {
    'Central': 492646.91,
    'East': 669518.73,
    'South': 389151.46,
    'West': 710219.68
}

# ============================================================================
# 차트 생성
# ============================================================================
# TODO: 여기에 코드를 작성하세요
# 1. 초기 막대 그래프 생성
# 2. updatemenus를 사용하여 버튼 추가
#    - "막대 그래프" 버튼: type='bar'
#    - "선 그래프" 버튼: type='scatter', mode='lines+markers'
#    - "파이 차트" 버튼: type='pie'
# 3. 각 버튼 클릭 시 해당 차트 타입으로 전환되도록 설정


fig = go.Figure(data=(go.Bar(x=list(region_sales.keys()), y=list(region_sales.values()))))
fig.update_layout(
  updatemenus = [
    dict(
      type='buttons',
      buttons = list([
        dict(
          args=['type', 'bar'],
          label='bar go',
          method="restyle"
        ),
        dict(
          args=['type', 'scatter'],
          label='scatter go',
          method='restyle'
        ),
        dict(
          args=['type', 'pie'],
          label='pie go',
          method='restyle'
        )
      ])
    )
  ]
)

fig.show()


fig_px = px.bar(x=list(region_sales.keys()), y=list(region_sales.values()))
fig_px.update_layout(
  width=600,
  height=400,
  updatemenus=[
    dict(
      type='buttons',
      buttons=list([
        dict(
          args=['type', 'bar'],
          label='bar px',
          method='restyle'
        ),
        dict(
          args=['type', 'scatter'],
          label='scetter',
          method='restyle'
        )
      ])
    )
  ]
)
fig_px.show()

# 힌트:
# - fig = go.Figure()로 figure 생성
# - fig.add_trace()로 초기 trace 추가
# - fig.update_layout(updatemenus=[...])로 버튼 추가
# - updatemenus의 각 버튼에서 method='restyle' 또는 method='update' 사용
# - args에 차트 타입 변경 정보 포함

# 예시 코드 구조:
# fig = go.Figure()
# fig.add_trace(go.Bar(...))
# fig.update_layout(
#     updatemenus=[
#         dict(
#             type="buttons",
#             direction="right",
#             x=0.7,
#             y=1.15,
#             buttons=list([
#                 dict(label="막대 그래프", method="restyle", args=[{"type": "bar"}]),
#                 dict(label="선 그래프", method="restyle", args=[{"type": "scatter", "mode": "lines+markers"}]),
#                 dict(label="파이 차트", method="restyle", args=[{"type": "pie"}]),
#             ])
#         )
#     ]
# )

# ============================================================================
# 결과 저장
# ============================================================================
# fig.write_html('result1_button.html')
# fig.show()

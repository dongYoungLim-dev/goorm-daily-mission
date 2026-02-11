"""
문제 1: Plotly 범례 (Legend)

목표: Plotly 차트의 범례를 커스터마이징하여 더 보기 좋고 정보가 명확한 차트 만들기
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
# ============================================================================
# 데이터 준비
# ============================================================================
# 여러 카테고리의 데이터 (범례 문제용)
# 이 데이터를 사용하는 이유:
# - Region, Category, Segment 세 가지 다른 분류 기준의 데이터를 사용하여
#   여러 trace를 한 차트에 표시할 수 있습니다
# - 각 trace마다 다른 범례 항목이 생성되어 범례 커스터마이징을 연습하기 좋습니다
# - 범례의 위치, 스타일, 클릭 기능 등을 테스트하기에 적합한 데이터 구조입니다
region_sales = {
    'Central': 492646.91,
    'East': 669518.73,
    'South': 389151.46,
    'West': 710219.68,
}

category_sales = {
    'Furniture': 728658.58,
    'Office Supplies': 705422.33,
    'Technology': 827455.87,
}

segment_sales = {
    'Consumer': 1148060.53,
    'Corporate': 688494.07,
    'Home Office': 424982.18,
}


px_data = px.data.tips()

# ============================================================================
# 차트 생성
# ============================================================================
# TODO: 여기에 코드를 작성하세요
# 1. 여러 trace를 추가하여 범례가 여러 개 나타나도록 하세요
#    - Region별 Sales 막대 그래프
#    - Category별 Sales 막대 그래프
#    - Segment별 Sales 막대 그래프


# px를 이용하면 범례는 자동으로 생성이 된다.

fig_px = px.scatter(
  px_data,
  x = 'total_bill',
  y = 'tip',
  color = 'sex',
  width = 600,
  height = 400,
)

fig = go.Figure()

fig.add_trace(
  go.Bar(
    x=list(region_sales.keys()),
    y=list(region_sales.values()),
    name='Region별 Sales'
  )
)
fig.add_trace(
  go.Bar(
    x=list(category_sales.keys()),
    y=list(category_sales.values()),
    name='Category별 Sales'
  )
)
fig.add_trace(
  go.Bar(
    x=list(segment_sales.keys()),
    y=list(segment_sales.values()),
    name='Segment별 Sales'
  )
)

# 2. 범례 커스터마이징:
#    - 위치: 오른쪽 상단 (x=1.02, y=1)
#    - 방향: 세로 (orientation='v')
#    - 배경색, 테두리색 등 스타일 설정
# fig.update_layout(showlegend=False) # 범례 숨기기
fig.update_layout(
  legend=dict(
    x = 1,
    y = 1,
    xanchor = 'center',
    yanchor = 'middle',
    orientation = 'v',
    bgcolor = 'rgba(255,255,255,0.8)',
    bordercolor = 'black',
    borderwidth = 1,
    title = 'Sales 비교 차트'
  )
)


# 3. 각 trace의 name 속성으로 범례 항목 이름 설정


fig.show()

# 힌트:
# - fig = go.Figure()로 figure 생성
# - fig.add_trace(go.Bar(..., name='범례 이름'))로 trace 추가
# - fig.update_layout(legend=dict(...))로 범례 설정
# - legend 속성: x, y, orientation, bgcolor, bordercolor, borderwidth 등

# 예시 코드 구조:
# fig = go.Figure()
# fig.add_trace(go.Bar(x=list(region_sales.keys()), y=list(region_sales.values()), name='Region별 Sales'))
# fig.add_trace(go.Bar(x=list(category_sales.keys()), y=list(category_sales.values()), name='Category별 Sales'))
# fig.add_trace(go.Bar(x=list(segment_sales.keys()), y=list(segment_sales.values()), name='Segment별 Sales'))
# 
# fig.update_layout(
#     legend=dict(
#         x=1.02,
#         y=1,
#         orientation='v',
#         bgcolor='rgba(255,255,255,0.8)',
#         bordercolor='black',
#         borderwidth=1
#     ),
#     title="Sales 비교 차트"
# )

# ============================================================================
# 결과 저장
# ============================================================================
# fig.write_html('result1_legend.html')
# fig.show()

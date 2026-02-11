"""
문제 2: Plotly 인터렉티브 드롭다운 (Dropdown)

목표: 드롭다운 메뉴를 사용하여 데이터를 필터링하는 인터렉티브 차트 만들기
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ============================================================================
# 데이터 준비
# ============================================================================
# Category별 Sales 합계 데이터
# 이 데이터를 사용하는 이유:
# - Category는 3개의 카테고리(Furniture, Office Supplies, Technology)로 구성되어
#   드롭다운으로 필터링하기에 적합한 구조입니다
# - 각 Category의 Sales 합계가 비슷한 수준(70만~82만)이어서 필터링 시
#   차이를 명확하게 비교할 수 있습니다
# - "전체" 옵션과 개별 Category 옵션을 통해 데이터의 부분집합을
#   효과적으로 시각화할 수 있습니다
category_sales = {
    'Furniture': 728658.58,
    'Office Supplies': 705422.33,
    'Technology': 827455.87
}

# ============================================================================
# 차트 생성
# ============================================================================
# TODO: 여기에 코드를 작성하세요
# 1. 각 Category별 막대 그래프 trace 생성 (총 4개: 전체 + 각 Category)
# 2. updatemenus를 사용하여 드롭다운 메뉴 추가
#    - type='dropdown' 설정
#    - "전체" 옵션: 모든 trace 표시
#    - "Furniture" 옵션: Furniture만 표시
#    - "Office Supplies" 옵션: Office Supplies만 표시
#    - "Technology" 옵션: Technology만 표시
# 3. visible 속성을 사용하여 각 옵션별로 표시할 trace 제어


fig = go.Figure()

# 각 Category별로 개별 trace 추가 (총 3개)
# "전체" 옵션은 모든 trace를 보여주는 것으로 처리
fig.add_trace(
    go.Bar(
        name='Furniture',
        x=['Furniture'],
        y=[category_sales['Furniture']],
    )
)
fig.add_trace(
    go.Bar(
        name='Office Supplies',
        x=['Office Supplies'],
        y=[category_sales['Office Supplies']],
    )
)
fig.add_trace(
    go.Bar(
        name='Technology',
        x=['Technology'],
        y=[category_sales['Technology']],
    )
)

# 드롭다운 메뉴 추가
fig.update_layout(
    updatemenus=[
        dict(
            type='dropdown',
            direction='down',
            x=0.1,
            y=1.15,
            buttons=list([
                dict(
                    label='전체', 
                    method='update',
                    args=[{'visible': [True, True, True]}, {'title': '전체'}]
                ),
                dict(
                    label='Furniture',
                    method='update',
                    args=[{'visible': [True, False, False]}, {'title': 'Furniture'}]
                ),
                dict(
                    label='Office Supplies',
                    method='update',
                    args=[{'visible': [False, True, False]}, {'title': 'Office Supplies'}]
                ),
                dict(
                    label='Technology',
                    method='update',
                    args=[{'visible': [False, False, True]}, {'title': 'Technology'}]
                )
            ])
        )
    ],
    title="Category별 Sales"
)

fig.show()










# 힌트:
# - fig = go.Figure()로 figure 생성
# - 각 Category별로 go.Bar trace 추가 (총 3개)
# - fig.update_layout(updatemenus=[...])로 드롭다운 추가
# - updatemenus의 type='dropdown' 설정
# - 각 버튼에서 visible 속성으로 trace 표시/숨김 제어
# - visible은 [True, False, False] 형태의 리스트로 각 trace의 표시 여부 지정

# 예시 코드 구조:
# fig = go.Figure()
# fig.add_trace(go.Bar(x=['Furniture'], y=[category_sales['Furniture']], name='Furniture'))
# fig.add_trace(go.Bar(x=['Office Supplies'], y=[category_sales['Office Supplies']], name='Office Supplies'))
# fig.add_trace(go.Bar(x=['Technology'], y=[category_sales['Technology']], name='Technology'))
# 
# fig.update_layout(
#     updatemenus=[
#         dict(
#             type="dropdown",
#             direction="down",
#             x=0.1,
#             y=1.15,
#             buttons=list([
#                 dict(label="전체", method="update", args=[{"visible": [True, True, True]}]),
#                 dict(label="Furniture", method="update", args=[{"visible": [True, False, False]}]),
#                 dict(label="Office Supplies", method="update", args=[{"visible": [False, True, False]}]),
#                 dict(label="Technology", method="update", args=[{"visible": [False, False, True]}]),
#             ])
#         )
#     ]
# )

# ============================================================================
# 결과 저장
# ============================================================================
# fig.write_html('result2_dropdown.html')
# fig.show()

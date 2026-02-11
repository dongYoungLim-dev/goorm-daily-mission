"""
문제 2: Plotly 템플릿 (Template)

목표: Plotly의 다양한 템플릿을 사용하여 차트의 스타일을 변경하기
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# ============================================================================
# 데이터 준비
# ============================================================================
# Category별 Sales 합계 데이터
# 이 데이터를 사용하는 이유:
# - 동일한 데이터로 여러 템플릿을 적용하여 스타일 차이를 비교하기 좋습니다
# - Category는 3개의 항목으로 구성되어 있어 템플릿의 시각적 차이를
#   명확하게 확인할 수 있습니다
# - 막대 그래프로 표시하면 각 템플릿의 색상, 배경, 그리드 스타일 등을
#   쉽게 비교할 수 있습니다
sales_data = {
    'Furniture': 728658.58,
    'Office Supplies': 705422.33,
    'Technology': 827455.87,
}

# ============================================================================
# 차트 생성
# ============================================================================
# TODO: 여기에 코드를 작성하세요
# 1. make_subplots를 사용하여 여러 차트를 한 화면에 배치
fig = make_subplots(rows=2, cols=3, subplot_titles=('plotly', 'plotly_white', 'plotly_dark', 'ggplot2', 'seaborn', 'simple_white'))

# 템플릿 종류 ['plotly', 'plotly_white', 'plotly_dark', 'ggplot2', 'seaborn', 'simple_white', 'presentation','xgridoff','ygridoff','gridoff']
pio.templates.default = 'plotly'


# 2. 동일한 데이터로 여러 템플릿 적용:
#    - plotly: 기본 템플릿
#    - plotly_white: 흰색 배경
#    - plotly_dark: 다크 모드
#    - ggplot2: ggplot2 스타일
#    - seaborn: seaborn 스타일


fig.add_trace(
  go.Bar(
    x=list(sales_data.keys()), 
    y=list(sales_data.values()),
  ),
  row=1, col=1
)
fig.add_trace(
  go.Bar(
    x=list(sales_data.keys()), 
    y=list(sales_data.values()),
  ),
  row=1, col=2 
)
fig.add_trace(
  go.Bar(
    x=list(sales_data.keys()), 
    y=list(sales_data.values()),
  ),
  row=1, col=3 
)
fig.add_trace(
  go.Bar(
    x=list(sales_data.keys()), 
    y=list(sales_data.values()),
  ),
  row=2, col=1 
)
fig.add_trace(
  go.Bar(
    x=list(sales_data.keys()), 
    y=list(sales_data.values()),
  ),
  row=2, col=2 
)
fig.add_trace(
  go.Bar(
    x = list(sales_data.keys()),
    y = list(sales_data.values()),
  ),
  row=2, col=3 
) 
fig.update_layout(template='presentation')

# Plotly의 fig(figure)는 레이아웃 단위로만 template을 적용할 수 있습니다. 즉, 
# "trace(서브플롯) 단위로 개별 템플릿 적용"은 지원하지 않고,
# fig.update_layout(template='템플릿명') 으로 figure 전체에 적용만 가능합니다.
# 만약 subplot별로 시각적으로 템플릿을 다르게 보이게 하고 싶다면,
# 각 템플릿별로 개별 Figure를 만든 뒤, 이미지를 따로 저장하거나
# 이미지로 합쳐서 보여주는 방법(예: PIL 등으로 이미지 병합)을 사용해야 합니다.

# 아래는 예시로, figure 전체에 템플릿을 한 번에 적용하는 코드입니다:
# fig.update_layout(template='plotly_white')

# subplot별로 trace를 추가한 뒤, 전체 figure에 템플릿을 적용하세요.
# 여러 figure를 별도로 생성해서 subplot처럼 배치하고 싶으면, 
# 개별 figure를 이미지로 저장해 후처리해야 합니다.
fig.show()


# 힌트:
# - fig = make_subplots(rows=2, cols=3, ...)로 subplot 생성
# - 각 subplot에 trace 추가 후 해당 subplot에만 템플릿 적용
# - fig.update_layout(template="템플릿명")로 전체 템플릿 설정
# - 또는 각 subplot별로 다른 템플릿을 적용하려면 각각의 figure를 만들고 합치기

# 예시 코드 구조 (각 subplot에 다른 템플릿 적용):
# templates = ['plotly', 'plotly_white', 'plotly_dark', 'ggplot2', 'seaborn', 'simple_white']
# fig = make_subplots(rows=2, cols=3, subplot_titles=templates)
# 
# for i, template in enumerate(templates):
#     row = (i // 3) + 1
#     col = (i % 3) + 1
#     fig.add_trace(go.Bar(x=list(sales_data.keys()), y=list(sales_data.values())), row=row, col=col)
#     # 각 subplot에 템플릿 적용 (전체 레이아웃에 적용하거나 개별적으로)

# 또는 더 간단한 방법:
# 각 템플릿별로 별도의 figure를 만들고 subplot으로 합치기

# ============================================================================
# 결과 저장
# ============================================================================
# fig.write_html('result2_template.html')
# fig.show()

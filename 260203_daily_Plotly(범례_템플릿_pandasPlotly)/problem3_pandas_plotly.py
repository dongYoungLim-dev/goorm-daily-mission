"""
문제 3: Pandas-Plotly 설정

목표: Pandas DataFrame을 Plotly와 직접 연동하여 간편하게 차트 생성하기
"""

import pandas as pd
import plotly.graph_objects as go

# ============================================================================
# 데이터 준비
# ============================================================================
# 월별 Sales 데이터
# 이 데이터를 사용하는 이유:
# - Pandas DataFrame의 기본 구조(인덱스와 값)를 활용하기 좋은 데이터입니다
# - 월별 데이터는 시계열 차트(선 그래프)와 막대 그래프 모두에 적합합니다
# - DataFrame의 plot() 메서드를 사용하여 다양한 차트 타입을 쉽게 생성할 수 있습니다
monthly_sales = {
    'Jan': 150000,
    'Feb': 180000,
    'Mar': 220000,
    'Apr': 200000,
    'May': 250000,
    'Jun': 280000
}

# DataFrame 생성
# 이 데이터를 사용하는 이유:
# - Pandas-Plotly 백엔드를 설정하면 DataFrame의 plot() 메서드가
#   Plotly figure를 반환하므로, Plotly의 모든 기능을 사용할 수 있습니다
# - 여러 컬럼이 있는 DataFrame을 만들면 여러 trace를 한 번에 생성할 수 있어
#   범례도 자동으로 생성됩니다
df = pd.DataFrame({
    'Sales': list(monthly_sales.values())
}, index=list(monthly_sales.keys()))

# ============================================================================
# Pandas-Plotly 백엔드 설정
# ============================================================================
# TODO: 여기에 코드를 작성하세요
# 1. Pandas-Plotly 백엔드 설정
#    - pd.options.plotting.backend = "plotly" 설정
pd.options.plotting.backend = "plotly"

# 2. DataFrame의 plot() 메서드 사용:
#    - 막대 그래프: df.plot(kind='bar')
#    - 선 그래프: df.plot(kind='line')
#    - 산점도: df.plot(kind='scatter', x='컬럼1', y='컬럼2')
fig_1 = df.plot(kind='bar')
fig_1.update_layout(xaxis_title='월', yaxis_title='Sales')

fig_2 = df.plot(kind='line')
fig_2.update_layout(xaxis_title='월', yaxis_title='Sales')

# 산점도는 x, y 두 컬럼이 필요하므로 Target 컬럼 추가
df_scatter = pd.DataFrame({
    'Sales': list(monthly_sales.values()),
    'Target': [200000] * 6  # 목표치 예시
}, index=list(monthly_sales.keys()))
fig_3 = df_scatter.plot(kind='scatter', x='Sales', y='Target')
fig_3.update_layout(xaxis_title='Sales', yaxis_title='Target')

# 3. 반환된 figure 객체에 Plotly 기능 적용:
#    - update_layout()로 레이아웃 설정
#    - update_traces()로 trace 스타일 설정
fig_1.update_layout(template='presentation')
fig_2.update_layout(template='simple_white')
fig_3.update_layout(template='ggplot2')

fig_1.show()
fig_2.show()
fig_3.show()

# 힌트:
# - import pandas as pd
# - pd.options.plotting.backend = "plotly" 설정
# - fig = df.plot(kind='bar')로 차트 생성
# - fig는 Plotly figure 객체이므로 update_layout() 등 사용 가능
# - 여러 컬럼이 있으면 자동으로 여러 trace 생성됨

# 예시 코드 구조:
# pd.options.plotting.backend = "plotly"
# 
# # 막대 그래프
# fig1 = df.plot(kind='bar', title='월별 Sales - 막대 그래프')
# fig1.update_layout(xaxis_title='월', yaxis_title='Sales')
# 
# # 선 그래프
# fig2 = df.plot(kind='line', title='월별 Sales - 선 그래프')
# fig2.update_layout(xaxis_title='월', yaxis_title='Sales')
# 
# # 여러 컬럼이 있는 경우 (범례 자동 생성)
# df2 = pd.DataFrame({
#     'Sales': list(monthly_sales.values()),
#     'Target': [200000] * 6
# }, index=list(monthly_sales.keys()))
# fig3 = df2.plot(kind='bar', title='Sales vs Target')
# fig3.update_layout(xaxis_title='월', yaxis_title='금액')

# ============================================================================
# 결과 저장
# ============================================================================
# fig.write_html('result3_pandas_plotly.html')
# fig.show()

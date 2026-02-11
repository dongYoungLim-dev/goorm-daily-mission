"""
문제 1: 지수가중함수(EWM)를 활용한 시계열 데이터 분석

목표: 시계열 데이터에 지수가중함수(Exponential Weighted Moving)를 적용하여 
      트렌드를 분석하고 평활화된 데이터를 생성하기

출제 의도:
1. EWM의 기본 개념과 시계열 데이터 평활화 방법 학습
2. span, halflife, alpha, com 등 다양한 파라미터의 차이와 효과 이해
3. adjust, ignore_na 파라미터의 동작 방식과 활용법 학습
4. 시계열 데이터 시각화를 통한 EWM 효과 비교 분석 능력 향상
"""

from tarfile import PAX_FIELDS
import pandas as pd
import numpy as np
from pandas.core.window import ewm
import plotly.graph_objects as go
import plotly.express as px
import os
from pathlib import Path
# ============================================================================
# Kaggle 데이터셋 다운로드 및 로드
# ============================================================================
"""
Kaggle 데이터셋 추천:
1. Apple Stock Price (AAPL)
   - URL: https://www.kaggle.com/datasets/dhruvildave/apple-stock-price
   - 다운로드 명령: kaggle datasets download -d dhruvildave/apple-stock-price
   - 압축 해제 후: unzip apple-stock-price.zip

2. Daily Climate Data
   - URL: https://www.kaggle.com/datasets/sumanthvrao/daily-climate-time-series-data
   - 다운로드 명령: kaggle datasets download -d sumanthvrao/daily-climate-time-series-data

3. Bitcoin Historical Data
   - URL: https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data
   - 다운로드 명령: kaggle datasets download -d mczielinski/bitcoin-historical-data

데이터 로드 예시 (AAPL 주가 데이터 기준):
"""
# 주석을 해제하고 실제 데이터 경로로 수정하세요
print(f"__file__: {__file__}")
current_div = os.path.dirname(__file__)
data_path = os.path.join(current_div, 'data', 'AAPL.csv')
df = pd.read_csv(data_path)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# ============================================================================
# 실습용 샘플 데이터 생성 (Kaggle 데이터가 없는 경우)
# ============================================================================
# 출제 의도: 시계열 데이터의 특성을 잘 보여주는 주가 데이터 사용
# - 시간에 따른 변화와 변동성을 명확하게 보여줌
# - EWM을 적용하면 단기 변동을 제거하고 장기 트렌드를 명확하게 볼 수 있음
# - 실제 금융 데이터이므로 실무에서 EWM이 어떻게 사용되는지 이해하기 좋음
# - 날짜가 불규칙하지 않아 EWM 계산이 명확함

# 사용할 데이터 설명:
# - Date: 시계열 인덱스 (날짜)
#   * 이 컬럼을 선택한 이유: 시계열 분석의 기본이 되는 시간 정보이며,
#     EWM은 시간 순서가 중요한 시계열 데이터에 적용하는 기법
# - Close: 종가 데이터 (EWM을 적용할 수치형 데이터)
#   * 이 컬럼을 선택한 이유: 주가 데이터는 변동성이 크고 트렌드가 명확하여
#     EWM의 평활화 효과를 시각적으로 확인하기 좋음

print("데이터 미리보기:")
print(df.head())
print(f"\n데이터 형태: {df.shape}")
print(f"\n데이터 기간: {df.index.min()} ~ {df.index.max()}")
print(f"\n종가 통계:")
print(df['Close'].describe())

# ============================================================================
# 문제 1-1: span 파라미터를 사용한 EWM 계산
# ============================================================================
"""
출제 의도:
- span은 EWM의 기간을 지정하는 가장 직관적인 방법
- span이 클수록 더 많은 과거 데이터를 고려하여 평활화 정도가 높아짐
- span과 alpha의 관계 이해 (span ≈ 2/(alpha) - 1)
"""
# TODO: span=10과 span=20을 각각 사용하여 EWM을 계산하고 비교하세요
# 힌트: df['Close'].ewm(span=10).mean()
#       df['Close'].ewm(span=20).mean()

# =============================================================================
# [지수가중이동평균(EWM, Exponentially Weighted Moving Average) 설명]
# -----------------------------------------------------------------------------
# - 지수가중이동평균(EWM)은 시계열 데이터에서 최근 관측값에 더 높은 가중치를 부여하여
#   데이터의 트렌드(추세)를 부드럽게 파악할 수 있게 하는 평활화(Smoothing) 기법입니다.
# - 오래된 데이터일수록 가중치가 지수적으로 감소하며, 최근 데이터에 민감하게 반응합니다.
# 
# [주요 특징]
# • 일반 이동평균(Simple Moving Average)보다 최근 값의 영향력이 크기 때문에 
#   신속하게 변화하는 트렌드를 포착하는 데 유리합니다.
# • 가중치 감쇠 속도는 파라미터(span, halflife, alpha, com) 중 하나로 조정할 수 있습니다.
# • Pandas의 .ewm() 메서드를 활용하여 편리하게 적용할 수 있습니다.
#
# [주요 파라미터 설명]
# - span    : 적용할 기간(window) 크기와 같은 직관적 파라미터 (값이 커질수록 더 평탄)
# - halflife: 가중치가 50%로 줄어드는 기간을 지정 (값이 작을수록 최근 데이터 영향 ↑)
# - alpha   : 직접 감쇠율(0 < alpha <= 1)을 지정 (값이 클수록 최근 데이터 영향 ↑)
# - com     : 가중치의 중심(com; center of mass)을 통해 조정
#
# [수식 구조]
# - 각 시점의 EWM은 다음과 같이 계산됩니다:
#     y_t = alpha * x_t + (1 - alpha) * y_{t-1}
#   여기서,
#     y_t: t시점의 평활값, x_t: t시점의 실제 관측값, 
#     alpha: 감쇠율(파라미터로 정해짐)
#
# [활용 예시]
# - 주가, 기상 데이터 등 변동성이 높은 시계열의 노이즈 제거
# - 단기 트렌드, 장기 트렌드 분리
# =============================================================================


# ewm: 지수가중이동평균(Exponentially Weighted Moving average)을 계산하는 메서드
#   - .ewm(span=10): 기간(span)이 10인 지수가중이동 윈도우를 생성
#   - .mean(): 해당 창(window)에서의 평균을 계산
#   - 최근 데이터에 더 높은 가중치를 부여하며, 오래된 데이터는 지수적으로 가중치가 작아짐

ewm_span10 = df['Close'].ewm(span=10).mean()
ewm_span20 = df['Close'].ewm(span=20).mean()

fig = px.line(x=df.index, y=df['Close'], title='AAPL_Close')
fig.add_trace(go.Scatter(x=df.index, y=ewm_span10, name='EWM span=10', mode='lines'))
fig.add_trace(go.Scatter(x=df.index, y=ewm_span20, name='EWM span=20', mode='lines'))
fig.show()
# ============================================================================
# 문제 1-2: halflife 파라미터를 사용한 EWM 계산
# ============================================================================
"""
출제 의도:
- halflife는 가중치가 절반으로 줄어드는 기간을 지정
- span과 halflife의 관계 이해 (span ≈ halflife / 0.5)
- 시간 기반 가중치 감쇠 개념 학습
"""
# TODO: halflife=5와 halflife=10을 각각 사용하여 EWM을 계산하고 비교하세요
# 힌트: df['Close'].ewm(halflife=5).mean()
#       df['Close'].ewm(halflife=10).mean()

ewm_halflife10 = df['Close'].ewm(halflife=10).mean()
ewm_halflife20 = df['Close'].ewm(halflife=20).mean()

fig_halflife = px.line(x=df.index, y=df['Close'], title='AAPL_Close')
fig_halflife.add_trace(go.Scatter(x=df.index, y=ewm_halflife10, name='EWM halflife=5', mode='lines'))
fig_halflife.add_trace(go.Scatter(x=df.index, y=ewm_halflife20, name='EWM halflife=10', mode='lines'))
fig_halflife.show()


# ============================================================================
# 문제 1-3: alpha 파라미터를 사용한 EWM 계산
# ============================================================================
"""
출제 의도:
- alpha는 직접 가중치 감쇠율을 지정 (0 < alpha <= 1)
- alpha가 클수록 최근 데이터에 더 높은 가중치 부여
- alpha와 span의 관계 이해 (alpha = 2/(span+1))
"""
# TODO: alpha=0.2와 alpha=0.5를 각각 사용하여 EWM을 계산하고 비교하세요
# 힌트: df['Close'].ewm(alpha=0.2).mean()
#       df['Close'].ewm(alpha=0.5).mean()

ewm_alpha02 = df['Close'].ewm(alpha=0.2).mean()
ewm_alpha05 = df['Close'].ewm(alpha=0.5).mean()

fig_alpha = px.line(x=df.index, y=df['Close'], title='AAPL_Close')
fig_alpha.add_trace(go.Scatter(x=df.index, y=ewm_alpha02, name='EWM alpha=0.2', mode='lines'))
fig_alpha.add_trace(go.Scatter(x=df.index, y=ewm_alpha05, name='EWM alpha=0.5', mode='lines'))
fig_alpha.show()
# ============================================================================
# 문제 1-4: com (center of mass) 파라미터를 사용한 EWM 계산
# ============================================================================
"""
출제 의도:
- com은 가중치의 중심점(center of mass)을 지정
- com이 클수록 더 많은 과거 데이터를 고려
- com과 span의 관계 이해 (com = (span-1)/2)
"""
# TODO: com=3과 com=7을 각각 사용하여 EWM을 계산하고 비교하세요
# 힌트: df['Close'].ewm(com=3).mean()
#       df['Close'].ewm(com=7).mean()

ewm_com3 = df['Close'].ewm(com=3).mean()
ewm_com7 = df['Close'].ewm(com=7).mean()

fig_com = px.line(x=df.index, y=df['Close'], title='AAPL_Close')
fig_com.add_trace(go.Scatter(x=df.index, y=ewm_com3, name='EWM com=3', mode='lines'))
fig_com.add_trace(go.Scatter(x=df.index, y=ewm_com7, name='EWM com=7', mode='lines'))
fig_com.show()
# ============================================================================
# 문제 1-5: adjust 파라미터 비교
# ============================================================================
"""
출제 의도:
- adjust=True (기본값): 가중치를 정규화하여 초기 값의 영향 감소
- adjust=False: 가중치를 정규화하지 않아 초기 값의 영향이 더 큼
- 두 방식의 수학적 차이와 실무에서의 선택 기준 이해
"""
# TODO: span=10을 사용하여 adjust=True와 adjust=False를 각각 적용하고 비교하세요
# 힌트: df['Close'].ewm(span=10, adjust=True).mean()
#       df['Close'].ewm(span=10, adjust=False).mean()

ewm_span10_adjustTrue = df['Close'].ewm(span=10, adjust=True).mean()
ewm_span10_adjustFalse = df['Close'].ewm(span=10, adjust=False).mean()

fig_adjust = px.line(x=df.index, y=df['Close'], title='AAPL_Close')
fig_adjust.add_trace(go.Scatter(x=df.index, y=ewm_span10_adjustTrue, name='EWM span=10 adjust=True', mode='lines'))
fig_adjust.add_trace(go.Scatter(x=df.index, y=ewm_span10_adjustFalse, name='EWM span=10 adjust=False', mode='lines'))
fig_adjust.show()
# ============================================================================
# 문제 1-6: ignore_na 파라미터 비교
# ============================================================================
"""
출제 의도:
- ignore_na=True (기본값): NaN 값을 무시하고 계산
- ignore_na=False: NaN 값을 0으로 간주하여 계산
- 결측치가 있는 시계열 데이터에서의 EWM 계산 방법 이해
"""
# 일부 데이터에 NaN 값 추가 (ignore_na 테스트용)
df_with_na = df.copy()
df_with_na.loc[df_with_na.sample(5).index, 'Close'] = np.nan

# TODO: span=10을 사용하여 ignore_na=True와 ignore_na=False를 각각 적용하고 비교하세요
# 힌트: df_with_na['Close'].ewm(span=10, ignore_na=True).mean()
#       df_with_na['Close'].ewm(span=10, ignore_na=False).mean()

ewm_span10_ignoreTrue = df_with_na['Close'].ewm(span=10, ignore_na=True).mean()
ewm_span10_ignoreFalse = df_with_na['Close'].ewm(span=10, ignore_na=False).mean()

fig_ignore = px.line(x=df_with_na.index, y=df_with_na['Close'], title='AAPL_Close')
fig_ignore.add_trace(go.Scatter(x=df_with_na.index, y=ewm_span10_ignoreTrue, name='EWM span=10 ignore=True', mode='lines'))
fig_ignore.add_trace(go.Scatter(x=df_with_na.index, y=ewm_span10_ignoreFalse, name='EWM span=10 ignore=False', mode='lines'))
fig_ignore.show()

# ============================================================================
# 문제 1-7: 여러 파라미터 조합으로 EWM 계산 및 비교
# ============================================================================
"""
출제 의도:
- 동일한 효과를 내는 다른 파라미터 조합 이해
- 예: span=20 ≈ halflife=10 ≈ alpha=0.095 ≈ com=9.5
- 상황에 맞는 파라미터 선택 능력 향상
"""
# TODO: 다음 파라미터들을 사용하여 EWM을 계산하고 결과를 비교하세요:
# - span=20
# - halflife=10
# - alpha=0.095
# - com=9.5
# 힌트: 각각 계산한 후 결과를 비교하여 유사한지 확인

ewm_span20 = df['Close'].ewm(span=20).mean()
ewm_halflife10 = df['Close'].ewm(halflife=10).mean()
ewm_alpha0095 = df['Close'].ewm(alpha=0.095).mean()
ewm_com95 = df['Close'].ewm(com=9.5).mean()

fig_compare = px.line(x=df.index, y=df['Close'], title='AAPL_Close')
fig_compare.add_trace(go.Scatter(x=df.index, y=ewm_span20, name='EWM span=20', mode='lines'))
fig_compare.add_trace(go.Scatter(x=df.index, y=ewm_halflife10, name='EWM halflife=10', mode='lines'))
fig_compare.add_trace(go.Scatter(x=df.index, y=ewm_alpha0095, name='EWM alpha=0.095', mode='lines'))
fig_compare.add_trace(go.Scatter(x=df.index, y=ewm_com95, name='EWM com=9.5', mode='lines'))
fig_compare.show()

# ============================================================================
# 문제 1-8: 원본 데이터와 EWM 결과 시각화
# ============================================================================
"""
출제 의도:
- 시각화를 통한 EWM의 평활화 효과 확인
- 여러 파라미터의 차이를 한눈에 비교
- 시계열 데이터 분석에서 시각화의 중요성 이해
"""
# TODO: 원본 데이터와 여러 EWM 결과를 하나의 차트에 시각화하세요
# 힌트:
# plt.figure(figsize=(12, 6))
# plt.plot(df.index, df['Close'], label='원본', alpha=0.5, linewidth=1)
# plt.plot(df.index, ewm_span10, label='EWM span=10')
# plt.plot(df.index, ewm_span20, label='EWM span=20')
# plt.legend()
# plt.title('AAPL 주가와 EWM 비교')
# plt.xlabel('Date')
# plt.ylabel('Close Price')
# plt.grid(True, alpha=0.3)
# plt.show()

ewm_span5 = df['Close'].ewm(span=5).mean()
ewm_span30 = df['Close'].ewm(span=30).mean()

fig_trend = px.line(x=df.index, y=df['Close'], title='AAPL_Close')
fig_trend.add_trace(go.Scatter(x=df.index, y=ewm_span5, name='EWM span=5', mode='lines'))
fig_trend.add_trace(go.Scatter(x=df.index, y=ewm_span30, name='EWM span=30', mode='lines'))
fig_trend.show()

# ============================================================================
# 문제 1-9: EWM을 활용한 트렌드 분석
# ============================================================================
"""
출제 의도:
- EWM을 사용하여 단기 변동을 제거하고 장기 트렌드 파악
- 여러 기간의 EWM을 비교하여 트렌드 변화 감지
# - 실무에서 사용하는 트렌드 분석 기법 학습
"""
# TODO: 짧은 기간(span=5)과 긴 기간(span=30)의 EWM을 계산하여
#       단기 트렌드와 장기 트렌드를 비교 분석하세요
# 힌트: 
# ewm_short = df['Close'].ewm(span=5).mean()
# ewm_long = df['Close'].ewm(span=30).mean()
# 트렌드 분석: ewm_short가 ewm_long보다 위에 있으면 상승 트렌드

returns = df['Close'].pct_change()
volatility = returns.ewm(span=10).std()

fig_volatility = px.line(x=df.index, y=volatility, title='AAPL_Volatility')
fig_volatility.show()

# ============================================================================
# 문제 1-10: EWM 기반 변동성 분석
# ============================================================================
"""
출제 의도:
- EWM을 사용하여 변동성을 계산하는 방법 학습
# - 표준편차나 분산의 EWM을 계산하여 변동성 추이 파악
# - 금융 데이터 분석에서 자주 사용되는 기법
"""
# TODO: EWM을 사용하여 변동성을 계산하세요
# 힌트: 
# returns = df['Close'].pct_change()  # 수익률 계산
# volatility = returns.ewm(span=10).std()  # EWM 기반 변동성

ewm_span10 = df['Close'].ewm(span=10).mean()
ewm_span20 = df['Close'].ewm(span=20).mean()
ewm_span30 = df['Close'].ewm(span=30).mean()
ewm_span40 = df['Close'].ewm(span=40).mean()
ewm_span50 = df['Close'].ewm(span=50).mean()
ewm_span60 = df['Close'].ewm(span=60).mean()
ewm_span70 = df['Close'].ewm(span=70).mean()
ewm_span80 = df['Close'].ewm(span=80).mean()  
ewm_span90 = df['Close'].ewm(span=90).mean()
ewm_span100 = df['Close'].ewm(span=100).mean()

fig_volatility = px.line(x=df.index, y=volatility, title='AAPL_Volatility')
fig_volatility.add_trace(go.Scatter(x=df.index, y=ewm_span10, name='EWM span=10', mode='lines'))
fig_volatility.add_trace(go.Scatter(x=df.index, y=ewm_span20, name='EWM span=20', mode='lines'))
fig_volatility.add_trace(go.Scatter(x=df.index, y=ewm_span30, name='EWM span=30', mode='lines'))
fig_volatility.add_trace(go.Scatter(x=df.index, y=ewm_span40, name='EWM span=40', mode='lines'))
fig_volatility.add_trace(go.Scatter(x=df.index, y=ewm_span50, name='EWM span=50', mode='lines'))
fig_volatility.add_trace(go.Scatter(x=df.index, y=ewm_span60, name='EWM span=60', mode='lines'))
fig_volatility.add_trace(go.Scatter(x=df.index, y=ewm_span70, name='EWM span=70', mode='lines'))
fig_volatility.add_trace(go.Scatter(x=df.index, y=ewm_span80, name='EWM span=80', mode='lines'))
fig_volatility.add_trace(go.Scatter(x=df.index, y=ewm_span90, name='EWM span=90', mode='lines'))
fig_volatility.add_trace(go.Scatter(x=df.index, y=ewm_span100, name='EWM span=100', mode='lines'))
fig_volatility.show()
# ============================================================================
# 문제 1-11: EWM 결과를 DataFrame에 추가
# ============================================================================
"""
출제 의도:
# - EWM 결과를 원본 데이터와 함께 저장하여 후속 분석에 활용
# - 여러 EWM 결과를 한 번에 관리하는 방법 학습
"""
# TODO: 여러 EWM 결과를 DataFrame에 새로운 컬럼으로 추가하세요
# 힌트:
# df['EWM_span10'] = df['Close'].ewm(span=10).mean()
# df['EWM_span20'] = df['Close'].ewm(span=20).mean()
# df['EWM_halflife10'] = df['Close'].ewm(halflife=10).mean()

df['EWM_span10'] = df['Close'].ewm(span=10).mean()
df['EWM_span20'] = df['Close'].ewm(span=20).mean()
df['EWM_halflife10'] = df['Close'].ewm(halflife=10).mean()
df['EWM_alpha0095'] = df['Close'].ewm(alpha=0.095).mean()
df['EWM_com95'] = df['Close'].ewm(com=9.5).mean()


df_ewm = pd.DataFrame({
    'Original': df['Close'],
    'EWM_span10': df['EWM_span10'],
    'EWM_span20': df['EWM_span20'],
    'EWM_halflife10': df['EWM_halflife10'],
    'EWM_alpha0095': df['EWM_alpha0095'],
    'EWM_com95': df['EWM_com95']
})

df_ewm.to_csv('result1_ewm.csv')
print(df_ewm.describe())

# ============================================================================
# 문제 1-12: EWM 결과 저장 및 요약 통계
# ============================================================================
"""
출제 의도:
- 분석 결과를 파일로 저장하는 방법 학습
- 원본 데이터와 EWM 결과의 통계적 비교
- 실무에서 사용하는 결과 보고서 작성 능력 향상
"""
# TODO: EWM 결과를 포함한 DataFrame을 CSV 파일로 저장하고,
#       원본과 EWM 결과의 요약 통계를 비교하세요
# 힌트:
# df_ewm = pd.DataFrame({
#     'Original': df['Close'],
#     'EWM_span10': df['Close'].ewm(span=10).mean(),
#     'EWM_span20': df['Close'].ewm(span=20).mean(),
# })
# df_ewm.to_csv('result1_ewm.csv')
# print(df_ewm.describe())

fig_compare = px.line(x=df.index, y=df['Close'], title='AAPL_Close')
fig_compare.add_trace(go.Scatter(x=df.index, y=df['EWM_span10'], name='EWM span=10', mode='lines'))
fig_compare.add_trace(go.Scatter(x=df.index, y=df['EWM_span20'], name='EWM span=20', mode='lines'))
fig_compare.add_trace(go.Scatter(x=df.index, y=df['EWM_halflife10'], name='EWM halflife=10', mode='lines'))
fig_compare.add_trace(go.Scatter(x=df.index, y=df['EWM_alpha0095'], name='EWM alpha=0.095', mode='lines'))
fig_compare.add_trace(go.Scatter(x=df.index, y=df['EWM_com95'], name='EWM com=9.5', mode='lines'))
fig_compare.show()

# ============================================================================
# 결과 확인
# ============================================================================
# 위의 문제들을 해결한 후 결과를 확인하세요
# print() 또는 to_csv()로 결과 저장하여 확인

print("\n문제 해결을 완료하세요!")
print("각 TODO 부분을 채워넣고 실행하여 결과를 확인하세요.")
print("\n추가 연습:")
print("- 각 파라미터의 차이를 시각화하여 비교해보세요")
print("- 실제 Kaggle 데이터를 사용하여 더 복잡한 시계열 분석을 수행해보세요")
print("- EWM을 활용한 트렌드 예측 모델을 만들어보세요")

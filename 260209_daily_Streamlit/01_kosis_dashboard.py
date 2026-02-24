import streamlit as st
import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(__file__)

@st.cache_data
def load_data():
  return pd.read_csv(os.path.join(SCRIPT_DIR, 'data', '시도_쌍태아_성별_출생_20260224214035.csv'), header=1)


df = load_data()

st.title('쌍태아 출행 현황 대시보드')
st.dataframe(df)

# ----- 사이드바: 선택값으로 차트 구성 변경 -----
# 1) 사이드바에 표시할 "지표" 목록 = DataFrame의 숫자 컬럼들 (시도별 제외)
#    df.columns[1:] 로 시도별을 빼고 "계(쌍)", "남자+남자(쌍)" 등만 사용
metric_options = list(df.columns[1:])

# 2) st.sidebar.selectbox: 사용자가 선택한 값이 selected_metric 변수에 담김
#    이 값을 이후 차트에서 "어떤 컬럼을 y축으로 그릴지"에 연결합니다
selected_metric = st.sidebar.selectbox(
    "표시할 지표",
    options=metric_options,
    index=0,
    help="선택한 지표별로 시도별 막대 차트가 바뀝니다.",
)

# 3) 데이터 연결: 선택값(selected_metric) → 차트용 데이터
#    - chart_df: 시도별을 인덱스로 두어 x축이 시도명이 되도록 함
#    - chart_df[selected_metric]: 사용자가 고른 지표 한 컬럼만 추출 → y축에 매핑
#    이렇게 사이드바 선택과 DataFrame 컬럼을 1:1로 연결하면 선택별로 차트가 변경됩니다
df = df.iloc[1:].reset_index(drop=True)
chart_df = df.set_index("시도별")
st.bar_chart(chart_df[selected_metric])
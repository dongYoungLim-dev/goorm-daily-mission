"""
문제 2 (난이도 조정 버전): GroupBy 기초 3문항

목표: Pandas의 GroupBy를 "기본 집계 → 다중 그룹 집계 → transform 활용" 흐름으로 익히기

출제 의도:
1. 가장 자주 쓰는 groupby 패턴(합계/평균/개수)을 먼저 익히기
2. 2개 컬럼(Region, Category) 기준으로 집계표를 만드는 방법 익히기
3. transform으로 "그룹 평균"을 원본 데이터에 붙이고 비교/필터링하기

진행 방법:
- 아래 3개의 TODO만 해결하면 됩니다.
- (선택) 추가 연습은 시간이 남을 때만 해도 됩니다.
"""

import pandas as pd
import numpy as np

# ============================================================================
# Kaggle 데이터셋 다운로드 및 로드
# ============================================================================
"""
Kaggle 데이터셋 추천:
1. Superstore Sales Dataset
   - URL: https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting
   - 다운로드 명령: kaggle datasets download -d rohitsahoo/sales-forecasting
   - 압축 해제 후: unzip sales-forecasting.zip

2. E-commerce Sales Data
   - URL: https://www.kaggle.com/datasets/carrie1/ecommerce-data
   - 다운로드 명령: kaggle datasets download -d carrie1/ecommerce-data

3. Retail Sales Dataset
   - URL: https://www.kaggle.com/datasets/manjeetsingh/retaildataset
   - 다운로드 명령: kaggle datasets download -d manjeetsingh/retaildataset

데이터 로드 예시 (Superstore Sales 기준):
"""
# 주석을 해제하고 실제 데이터 경로로 수정하세요
# df = pd.read_csv('data/train.csv')

# ============================================================================
# 실습용 샘플 데이터 생성 (Kaggle 데이터가 없는 경우)
# ============================================================================
# 출제 의도: 그룹화 연습에 적합한 다양한 카테고리와 수치형 데이터 포함
# - Region, Category, Sub-Category 등 여러 그룹화 기준 제공
# - Sales, Quantity, Profit 등 집계 가능한 수치형 데이터 포함
# - 일부 NaN 값 포함하여 dropna 파라미터 테스트 가능

np.random.seed(42)
n_records = 1000

# 그룹화 기준 컬럼들
regions = ['North', 'South', 'East', 'West']
categories = ['Furniture', 'Office Supplies', 'Technology']
sub_categories = ['Chairs', 'Tables', 'Phones', 'Accessories', 'Binders', 'Paper']

df = pd.DataFrame({
    'OrderID': range(1, n_records + 1),
    'Region': np.random.choice(regions, n_records),
    'Category': np.random.choice(categories, n_records),
    'SubCategory': np.random.choice(sub_categories, n_records),
    'Sales': np.random.uniform(10, 1000, n_records),
    'Quantity': np.random.randint(1, 10, n_records),
    'Profit': np.random.uniform(-50, 200, n_records),
    'Year': np.random.choice([2020, 2021, 2022], n_records),
    'Month': np.random.randint(1, 13, n_records)
})

# 일부 데이터에 NaN 값 추가 (dropna 테스트용)
df.loc[df.sample(50).index, 'Region'] = np.nan
df.loc[df.sample(30).index, 'Category'] = np.nan

# 사용할 데이터 설명:
# - Region: 지역 그룹화 기준 (4개 카테고리)
#   * 이 컬럼을 선택한 이유: 그룹 수가 적당하여 결과 비교가 용이하고,
#     비즈니스 분석에서 자주 사용되는 그룹화 기준
# - Category: 상품 카테고리 그룹화 기준 (3개 카테고리)
#   * 이 컬럼을 선택한 이유: 멀티 레벨 그룹화 연습에 적합하며,
#     계층적 데이터 구조 이해에 도움
# - SubCategory: 세부 카테고리 (멀티 레벨 그룹화용)
# - Sales, Quantity, Profit: 집계할 수치형 데이터
#   * 이 컬럼들을 선택한 이유: sum, mean, std 등 다양한 집계 함수 연습 가능
# - Year, Month: 시간 기반 그룹화 연습용
# - Region, Category에 일부 NaN 값 포함: dropna 파라미터 테스트용

print("데이터 미리보기:")
print(df.head())
print(f"\n데이터 형태: {df.shape}")
print(f"\n컬럼별 결측치:")
print(df.isnull().sum())
print(f"\nRegion 고유값: {df['Region'].value_counts(dropna=False)}")
print(f"\nCategory 고유값: {df['Category'].value_counts(dropna=False)}")

# ============================================================================
# 문제 2-1: Region별 "주문 수"와 "매출 합계" 집계하기 (기본)
# ============================================================================
"""
출제 의도:
- groupby의 가장 기본인 count/sum 집계를 연습
- 결과를 표(DataFrame) 형태로 깔끔하게 만드는 연습 (as_index=False)
"""
# TODO:
# 1) Region별로 레코드 수(=주문 수)와 Sales 합계를 구하세요.
# 2) 결과는 DataFrame으로 만들고, 컬럼 이름을 아래처럼 맞추세요.
#    - Region
#    - order_count
#    - sales_sum
#
# 힌트:
# - df.groupby('Region', as_index=False).agg(...)
# - 레코드 수는 'OrderID'의 count(또는 size)로 계산해도 됩니다.

result_2_1 = df.groupby('Region', as_index=False)


result_2_1_1 = result_2_1.agg(
  order_count=('OrderID', 'count'),
  sales_sum=('Sales', 'sum'),
)
print('-'*60)
print(result_2_1_1)

'''
# 결과
  Region  order_count      sales_sum
0   East          227  107153.303268
1  North          239  118189.610587
2  South          217  114380.387656
3   West          267  138135.397749
'''


# ============================================================================
# 문제 2-2: Region + Category 2단 그룹 집계표 만들기 (agg 연습)
# ============================================================================
"""
출제 의도:
- 2개 기준(Region, Category)으로 그룹화하는 멀티 그룹 집계를 연습
- agg로 여러 수치 컬럼을 한 번에 요약하는 연습
"""
# TODO:
# 1) Region과 Category를 동시에 그룹화해서 아래 집계값을 구하세요.
#    - Sales_mean: Sales 평균
#    - Profit_mean: Profit 평균
#    - Quantity_sum: Quantity 합계
# 2) 결측치(Region/Category가 NaN인 행)는 분석에서 제외해도 됩니다.
#
# 힌트:
# - df2 = df.dropna(subset=['Region', 'Category'])
# - df2.groupby(['Region', 'Category'], as_index=False).agg(...)

result_2_2 = df.dropna(subset=['Region', 'Category']) # 두 열(column)에 대한 결측치 행 제거
result_2_2_1 = result_2_2.groupby(by=['Region', 'Category'], as_index=False).agg(
  Sales_mean=('Sales', 'mean'),
  Profit_mean=('Profit', 'mean'),
  Quantity_sum=('Quantity', 'sum')
)
print('-'*60)
print(result_2_2_1)

# ============================================================================
# 문제 2-3: transform으로 "그룹 평균" 붙이고, 평균보다 큰 행만 뽑기
# ============================================================================
"""
출제 의도:
- transform을 사용하면 그룹별 통계값을 "원본 행 개수 그대로" 되돌릴 수 있음을 이해
- "내 그룹 평균보다 큰 값"처럼 실무에서 자주 하는 비교/필터링 패턴 연습
"""
# TODO:
# 1) Region별 Sales 평균을 각 행에 붙여서 새 컬럼 `RegionSalesMean`을 만드세요.
# 2) Sales가 RegionSalesMean보다 큰 행만 필터링해서 `df_above_mean`으로 만드세요.
# 3) df_above_mean에서 필요한 컬럼 몇 개만 골라 출력해보세요.
#
# 힌트:
# - df3 = df.dropna(subset=['Region'])
# - df3['RegionSalesMean'] = df3.groupby('Region')['Sales'].transform('mean')
# - df_above_mean = df3[df3['Sales'] > df3['RegionSalesMean']]

df_above_dropna = df.dropna(subset=['Region']).copy()
df_above_dropna['RegionSalesMean'] = df_above_dropna.groupby(by='Region', as_index=False)['Sales'].transform('mean') # 각 그룹별 평균값을 만든다.

# 방법 1: boolean 인덱싱 사용 (행 단위 필터링) - 추천!
df_above_mean = df_above_dropna[df_above_dropna['Sales'] > df_above_dropna['RegionSalesMean']]

# 방법 2: filter() 사용 (그룹 단위 필터링) - 현재 문제에는 부적합
# filter()는 그룹 전체를 포함할지 결정하므로, 단일 boolean을 반환해야 함
# 예시: Region별 평균 Sales가 400 이상인 Region의 모든 행 선택
# df_above_mean = df_above_dropna.groupby('Region').filter(
#     lambda group: group['Sales'].mean() >= 400  # 그룹 평균이 400 이상인 그룹만
# )

print('-'*60)
print(df_above_mean[['OrderID', 'Region', 'Sales', 'RegionSalesMean']].head(10))

print("\n문제(난이도 조정 버전) 3문항을 완료하세요!")
print("각 TODO 부분을 채워넣고 실행하여 결과를 확인하세요.")

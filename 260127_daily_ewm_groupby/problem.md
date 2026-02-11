# 2026년 1월 27일 데일리 미션

## 참고 자료
- Pandas EWM 공식 문서: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html
- Pandas GroupBy 공식 문서: https://pandas.pydata.org/docs/reference/groupby.html
- Kaggle 데이터셋: https://www.kaggle.com/datasets

---

## 문제 1: 지수가중함수(EWM)를 활용한 시계열 데이터 분석

### 목표
시계열 데이터에 지수가중함수(Exponential Weighted Moving)를 적용하여 트렌드를 분석하고 평활화된 데이터를 생성해보세요.

### Kaggle 데이터셋 추천
- **추천 1**: [Apple Stock Price (AAPL)](https://www.kaggle.com/datasets/dhruvildave/apple-stock-price)
  - 다운로드: `kaggle datasets download -d dhruvildave/apple-stock-price`
- **추천 2**: [Daily Climate Data](https://www.kaggle.com/datasets/sumanthvrao/daily-climate-time-series-data)
  - 다운로드: `kaggle datasets download -d sumanthvrao/daily-climate-time-series-data`
- **추천 3**: [Bitcoin Historical Data](https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data)
  - 다운로드: `kaggle datasets download -d mczielinski/bitcoin-historical-data`

### 요구사항
1. Kaggle에서 시계열 데이터를 다운로드하고 로드합니다.
2. 날짜/시간 컬럼을 인덱스로 설정합니다.
3. **EWM을 활용**하여 다음을 수행하세요:
   - `span`, `halflife`, `alpha` 파라미터를 각각 사용하여 EWM 계산
   - 원본 데이터와 EWM 결과를 비교하는 시각화
   - 여러 `com` (center of mass) 값으로 비교
4. EWM의 `adjust`, `ignore_na` 파라미터의 차이를 이해하고 적용해보세요.
5. 결과를 시각화하여 원본 데이터와 평활화된 데이터를 비교하세요.

### 힌트
- `df.ewm(span=20).mean()` - span 기반 EWM
- `df.ewm(halflife=10).mean()` - half-life 기반 EWM
- `df.ewm(alpha=0.3).mean()` - alpha 기반 EWM
- `df.ewm(com=5).mean()` - center of mass 기반 EWM
- `adjust=True` (기본값) vs `adjust=False`의 차이
- `ignore_na=True` vs `ignore_na=False`의 차이

### 예상 결과
- 원본 시계열 데이터와 여러 EWM 파라미터로 평활화된 데이터의 비교 차트
- 각 파라미터의 효과를 이해할 수 있는 시각화

---

## 문제 2: 그룹화 계산(GroupBy) 파라미터 활용

### 목표
Pandas의 GroupBy를 **기초 3문항**으로 연습해보세요. (난이도: 초급~초중급)

### Kaggle 데이터셋 추천
- **추천 1**: [Superstore Sales Dataset](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting)
  - 다운로드: `kaggle datasets download -d rohitsahoo/sales-forecasting`
- **추천 2**: [E-commerce Sales Data](https://www.kaggle.com/datasets/carrie1/ecommerce-data)
  - 다운로드: `kaggle datasets download -d carrie1/ecommerce-data`
- **추천 3**: [Retail Sales Dataset](https://www.kaggle.com/datasets/manjeetsingh/retaildataset)
  - 다운로드: `kaggle datasets download -d manjeetsingh/retaildataset`

### 요구사항
1. Kaggle에서 그룹화 가능한 데이터를 다운로드하고 로드합니다.
2. 아래 3가지를 순서대로 수행하세요.
   - **문항 1**: `Region`별 **레코드 수(count)** 와 **Sales 합계(sum)** 집계
   - **문항 2**: `Region` + `Category` **2단 그룹**으로 `Sales` 평균, `Profit` 평균, `Quantity` 합계 집계 (`agg` 사용)
   - **문항 3**: `transform`으로 `Region`별 `Sales` 평균을 각 행에 붙이고, **그 평균보다 Sales가 큰 행만** 필터링

### 힌트
- `df.groupby('Region', as_index=False).agg(...)`
- `df.groupby(['Region', 'Category'], as_index=False).agg(...)`
- `df.groupby('Region')['Sales'].transform('mean')`

### 예상 결과
- Region별 요약 테이블
- Region+Category 집계표
- transform을 이용한 “그룹 평균 대비” 필터링 결과

---

## 제출 형식

각 문제에 대해 별도의 Python 파일을 생성하세요:
- `problem1_ewm.py`: 문제 1 해결 코드
- `problem2_groupby.py`: 문제 2 해결 코드

각 파일은 독립적으로 실행 가능해야 하며, 데이터 로드부터 결과 출력까지 포함되어야 합니다.

---

## 난이도 안내
- **초급 → 중급**: 기본 Pandas 사용법을 알고 있으면서, EWM과 GroupBy의 고급 파라미터를 처음 접하는 수준
- 각 문제는 단계별로 해결 가능하며, 공식 문서를 참고하여 구현할 수 있습니다.

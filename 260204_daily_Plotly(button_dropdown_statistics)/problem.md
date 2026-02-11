# 2026년 2월 4일 데일리 미션

## 참고 자료
- URL: https://wikidocs.net/187235 (5-1 ~ 5-3 섹션 참고)

## 데이터
- `data/train.csv`: 판매 데이터 (Order ID, Order Date, Sales, Category, Sub-Category, Region 등 포함)

---

## 문제 1: Plotly 인터렉티브 버튼 (Button)

### 목표
버튼을 클릭하여 차트 타입을 변경할 수 있는 인터렉티브 차트를 만들어보세요.

### 요구사항
1. `train.csv` 데이터를 읽어옵니다.
2. **Region별 Sales 합계**를 계산합니다.
3. Plotly를 사용하여 막대 그래프(bar chart)를 생성합니다.
4. **버튼을 추가**하여 다음 기능을 구현하세요:
   - "막대 그래프" 버튼: 막대 그래프로 표시
   - "선 그래프" 버튼: 선 그래프(scatter with lines)로 표시
   - "파이 차트" 버튼: 파이 차트로 표시
5. `updatemenus`를 사용하여 버튼을 구현하세요.
6. 각 버튼 클릭 시 해당 차트 타입으로 전환되어야 합니다.

### 힌트
- `fig.update_layout(updatemenus=[...])` 사용
- `method="restyle"` 또는 `method="update"` 사용
- `args`에 차트 타입(`type`) 변경 정보 포함

### 예상 결과
- 3개의 버튼이 있는 인터렉티브 차트
- 버튼 클릭 시 차트 타입이 즉시 변경됨

---

## 문제 2: Plotly 인터렉티브 드롭다운 (Dropdown)

### 목표
드롭다운 메뉴를 사용하여 데이터를 필터링하는 인터렉티브 차트를 만들어보세요.

### 요구사항
1. `train.csv` 데이터를 읽어옵니다.
2. **Category별 Sales 합계**를 계산합니다.
3. Plotly를 사용하여 막대 그래프를 생성합니다.
4. **드롭다운 메뉴를 추가**하여 다음 기능을 구현하세요:
   - "전체" 옵션: 모든 Category 표시
   - "Furniture" 옵션: Furniture만 표시
   - "Office Supplies" 옵션: Office Supplies만 표시
   - "Technology" 옵션: Technology만 표시
5. 드롭다운 선택 시 해당 Category의 데이터만 차트에 표시되어야 합니다.
6. `updatemenus`의 `type="dropdown"`을 사용하세요.

### 힌트
- `updatemenus`에 `type="dropdown"` 설정
- `visible` 속성을 사용하여 데이터 표시/숨김 제어
- 각 옵션마다 다른 `visible` 배열 설정

### 예상 결과
- 드롭다운 메뉴가 있는 인터렉티브 차트
- 드롭다운 선택 시 해당 Category만 필터링되어 표시됨

---

## 문제 3: Plotly Statistics Chart

### 목표
통계 차트를 사용하여 데이터의 분포를 시각화해보세요.

### 요구사항
1. `train.csv` 데이터를 읽어옵니다.
2. **Category별 Sales 분포**를 분석합니다.
3. 다음 통계 차트를 각각 생성하세요:
   - **박스 플롯(Box Plot)**: Category별 Sales 분포를 박스 플롯으로 표시
   - **바이올린 플롯(Violin Plot)**: Category별 Sales 분포를 바이올린 플롯으로 표시
   - **히스토그램(Histogram)**: 전체 Sales의 분포를 히스토그램으로 표시 (subplot 사용)
4. 각 차트에 적절한 제목, 축 레이블을 추가하세요.
5. 박스 플롯과 바이올린 플롯은 같은 figure에 subplot으로 배치하세요.

### 힌트
- `plotly.graph_objects.Box` 또는 `plotly.express.box` 사용
- `plotly.graph_objects.Violin` 또는 `plotly.express.violin` 사용
- `plotly.graph_objects.Histogram` 또는 `plotly.express.histogram` 사용
- `make_subplots`를 사용하여 여러 차트를 한 figure에 배치

### 예상 결과
- Category별 Sales 분포를 보여주는 박스 플롯
- Category별 Sales 분포를 보여주는 바이올린 플롯
- 전체 Sales 분포를 보여주는 히스토그램
- 적절한 제목과 레이블이 있는 통계 차트

---

## 제출 형식

각 문제에 대해 별도의 Python 파일을 생성하세요:
- `problem1_button.py`: 문제 1 해결 코드
- `problem2_dropdown.py`: 문제 2 해결 코드
- `problem3_statistics.py`: 문제 3 해결 코드

각 파일은 독립적으로 실행 가능해야 하며, HTML 파일로 저장하여 결과를 확인할 수 있어야 합니다.

### 실행 예시
```python
# 각 파일에서
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 데이터 로드
df = pd.read_csv('data/train.csv')

# 차트 생성 및 저장
fig.write_html('result1_button.html')
```

---

## 난이도 안내
- **초급 → 중급**: 기본 Plotly 사용법을 알고 있으면서, 인터렉티브 기능과 통계 차트를 처음 접하는 수준
- 각 문제는 단계별로 해결 가능하며, 참고 URL의 예제를 참고하여 구현할 수 있습니다.

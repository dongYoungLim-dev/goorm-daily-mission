# 2026년 2월 3일 데일리 미션

## 참고 자료
- Plotly 공식 문서: https://plotly.com/python/
- Plotly 범례(Legend): https://plotly.com/python/legend/
- Plotly 템플릿: https://plotly.com/python/templates/
- Pandas-Plotly 통합: https://plotly.com/python/pandas-backend/

## 데이터
- `data/train.csv`: 판매 데이터 (Order ID, Order Date, Sales, Category, Sub-Category, Region, Segment 등 포함)

---

## 문제 1: Plotly 범례 (Legend)

### 목표
Plotly 차트의 범례를 커스터마이징하여 더 보기 좋고 정보가 명확한 차트를 만들어보세요.

### 요구사항
1. 여러 카테고리의 데이터를 하나의 차트에 표시합니다.
2. **범례의 위치, 스타일, 표시 방식을 조정**하세요:
   - 범례 위치: 오른쪽 상단
   - 범례 방향: 세로로 배치
   - 범례 항목 클릭 시 해당 trace 숨김/표시 기능
   - 범례 항목 이름 커스터마이징
3. 여러 trace를 추가하여 범례가 여러 개 나타나도록 하세요.
4. `update_layout`의 `legend` 파라미터를 사용하세요.

### 힌트
- `fig.update_layout(legend=dict(...))` 사용
- `x`, `y`, `orientation`, `bgcolor`, `bordercolor` 등 속성 활용
- `trace`의 `name` 속성으로 범례 항목 이름 설정

### 예상 결과
- 여러 trace가 있는 차트
- 범례가 오른쪽 상단에 세로로 배치됨
- 범례 항목 클릭 시 해당 데이터가 숨김/표시됨

---

## 문제 2: Plotly 템플릿 (Template)

### 목표
Plotly의 다양한 템플릿을 사용하여 차트의 스타일을 변경해보세요.

### 요구사항
1. 동일한 데이터로 여러 차트를 생성합니다.
2. **다양한 템플릿을 적용**하세요:
   - `plotly`: 기본 템플릿
   - `plotly_white`: 흰색 배경
   - `plotly_dark`: 다크 모드
   - `ggplot2`: ggplot2 스타일
   - `seaborn`: seaborn 스타일
3. 각 템플릿의 차이점을 비교할 수 있도록 subplot으로 배치하세요.
4. `template` 파라미터를 사용하세요.

### 힌트
- `fig.update_layout(template="템플릿명")` 사용
- `make_subplots`를 사용하여 여러 차트를 한 화면에 배치
- 사용 가능한 템플릿: `plotly`, `plotly_white`, `plotly_dark`, `ggplot2`, `seaborn`, `simple_white`, `presentation` 등

### 예상 결과
- 동일한 데이터로 여러 템플릿이 적용된 차트
- 각 템플릿의 스타일 차이를 비교할 수 있음

---

## 문제 3: Pandas-Plotly 설정

### 목표
Pandas DataFrame을 Plotly와 직접 연동하여 간편하게 차트를 생성해보세요.

### 요구사항
1. Pandas DataFrame을 생성합니다.
2. **Pandas-Plotly 백엔드를 설정**하세요:
   - `pd.options.plotting.backend = "plotly"` 설정
   - DataFrame의 `plot()` 메서드를 사용하여 차트 생성
3. 여러 종류의 차트를 생성하세요:
   - 막대 그래프 (bar)
   - 선 그래프 (line)
   - 산점도 (scatter)
4. Plotly의 기능(범례, 레이아웃 등)도 함께 사용하세요.

### 힌트
- `import pandas as pd`
- `pd.options.plotting.backend = "plotly"` 설정
- `df.plot(kind='bar')`, `df.plot(kind='line')` 등 사용
- 반환된 figure 객체에 `update_layout()` 등 적용 가능

### 예상 결과
- Pandas DataFrame을 직접 plot() 메서드로 차트 생성
- Plotly의 모든 기능을 사용할 수 있음

---

## 제출 형식

각 문제에 대해 별도의 Python 파일을 생성하세요:
- `problem1_legend.py`: 문제 1 해결 코드
- `problem2_template.py`: 문제 2 해결 코드
- `problem3_pandas_plotly.py`: 문제 3 해결 코드

각 파일은 독립적으로 실행 가능해야 하며, HTML 파일로 저장하여 결과를 확인할 수 있어야 합니다.

### 실행 예시
```python
# 각 파일에서
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 차트 생성 및 저장
fig.write_html('result1_legend.html')
```

---

## 난이도 안내
- **초급 → 중급**: 기본 Plotly 사용법을 알고 있으면서, 범례, 템플릿, Pandas 통합 기능을 처음 접하는 수준
- 각 문제는 단계별로 해결 가능하며, 참고 URL의 예제를 참고하여 구현할 수 있습니다.

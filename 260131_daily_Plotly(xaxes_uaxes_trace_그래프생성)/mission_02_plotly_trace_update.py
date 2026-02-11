"""
1. 미션 내용
- Plotly trace 업데이트

2. 해당 미션을 통해 학습 문제 2문제 (임의로 작성)
- Q1) `fig.update_traces()`와 `fig.data[i].update()`는 무엇이 다르고, 언제 각각이 더 적합한가요?
- Q2) 같은 figure 안에서 여러 trace를 추가한 뒤(trace마다 색/마커/선 스타일 다르게),
      특정 trace만 선택해서 스타일을 바꾸는 방법을 정리해보세요.

3. keggle 데이터 링크
- https://www.kaggle.com/datasets/spscientist/students-performance-in-exams
"""

import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

df_students = pd.read_csv('/Users/dymacpro/myProject/myDev/My/goorm-ai-study/260131_plotly/data/mission_02_students_performance/StudentsPerformance.csv')


def main() -> None:
    # TODO: 점수 컬럼(예: math score)을 히스토그램으로 그린 뒤,
    # trace 업데이트로 색/투명도/테두리 등을 바꿔보기
    fig = go.Figure()
    # fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 4, 2], mode="markers", name="raw"))
    fig.add_trace(go.Histogram(x=df_students['math score'], name="math score"))
    fig.add_trace(go.Histogram(x=df_students['reading score'], name="reading score"))
    fig.add_trace(go.Histogram(x=df_students['writing score'], name="writing score"))

    # 예시: 전체 trace 스타일 업데이트
    # fig.update_traces(marker=dict(size=12, opacity=0.7))
    # fig.update_traces(marker=dict(color='red', opacity=0.5))


    '''
    update_traces: 모든 trace에 대해 동일한 스타일 적용
    update_traces의 selector은 data[i].update와 동일한 결과를 가져온다.
    data[i].update: 특정 trace에 대해 스타일 적용

    selector과 data[i].update는 동일한 결과를 가져오지만, selector는 특정 trace name 값을 가지고 변경하기 때문에 좀더 직관적이다.
    data[i].update는 특정 trace index 값을 가지고 변경하기 때문에 trace가 추가되거나 삭제로 순서가 변경되면 의도와 다르게 적용되거나 오류가 발생할 수 있다. 
    '''


    # update_traces 
    fig.update_traces(marker=dict(line_width=2, line_color='black'))
    # fig.update_traces(selector=dict(name='math score'), marker=dict(color='red', opacity=0.4))
    # fig.update_traces(selector=dict(name='reading score'), marker=dict(color='blue', opacity=0.4))
    # fig.update_traces(selector=dict(name='writing score'), marker=dict(color='green', opacity=0.4))
    # data[i].update
    fig.data[0].update(marker=dict(color='red', opacity=0.4))
    fig.data[1].update(marker=dict(color='blue', opacity=0.4))
    fig.data[2].update(marker=dict(color='green', opacity=0.4))
    
    fig.update_layout(barmode='overlay')
    fig.update_layout(bargap=0.2)
    fig.update_layout(title="Mission 02: Update Traces")



    fig.show()


if __name__ == "__main__":
    main()


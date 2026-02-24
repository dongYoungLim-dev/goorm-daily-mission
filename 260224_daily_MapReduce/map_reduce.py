# =============================================================================
# MapReduce - 기능 설명 및 구현 순서
# =============================================================================
#
# [1] MapReduce란
#     - 대용량 데이터를 분산·병렬 처리하기 위한 프로그래밍 모델 (Google 논문 기반)
#     - Map 단계에서 입력을 변환하고, Reduce 단계에서 키별로 집계함
#     - Hadoop, Spark 등 분산 처리 프레임워크의 기본 아이디어
#
# [2] Map 단계
#     - 입력 데이터의 각 항목을 (key, value) 쌍으로 변환
#     - 예: 문장 "hello world" → ("hello", 1), ("world", 1)
#     - 각 레코드는 독립적으로 변환 가능 → 병렬 처리에 적합
#
# [3] Shuffle 단계
#     - 같은 key를 가진 (key, value)들을 묶어서 key별로 value 리스트를 만듦
#     - 예: ("hello", 1), ("hello", 1) → "hello": [1, 1]
#     - 실제 분산 시스템에서는 네트워크를 통해 같은 키를 가진 데이터를 한 노드로 모음
#
# [4] Reduce 단계
#     - 각 key에 대해 value 리스트를 하나의 결과로 합침
#     - 예: ("hello", [1, 1, 1]) → ("hello", 3)
#     - 집계 방식은 reduce_fn에 따라 합계, 평균, 리스트 병합 등으로 다양함
#
# [5] 구현 순서 요약
#     ① Map 함수 정의: 항목 하나를 (key, value) 리스트로 변환
#     ② Shuffle: Map 결과를 key별로 그룹화 (pandas DataFrame·groupby 사용)
#     ③ Reduce 함수 정의: (key, values) → (key, 최종값)
#     ④ run_map_reduce(data, map_fn, reduce_fn) 형태로 파이프라인 구성
#     ⑤ Word Count 예제로 동작 확인
# =============================================================================

# pandas: Map 결과를 테이블(DataFrame)로 다루고, groupby로 Shuffle/Reduce 수행에 사용
import pandas as pd


# -----------------------------------------------------------------------------
# ① Map 단계: 각 입력 항목을 (key, value) 쌍들의 리스트로 변환한 뒤 DataFrame으로 반환
# -----------------------------------------------------------------------------
# data: 입력 데이터 리스트 (예: 문장들의 리스트)
# map_fn: 항목 하나를 받아 (key, value) 튜플들의 리스트를 반환하는 함수
# 반환: (key, value)들을 담은 pandas DataFrame (columns: key, value)
def map_phase(data, map_fn):
    mapped = []
    for item in data:
        mapped.extend(map_fn(item))
    if not mapped:
        return pd.DataFrame(columns=["key", "value"]) # mapped 가 비어 있으면 빈 DataFrame을 만들다.
    return pd.DataFrame(mapped, columns=["key", "value"]) # mapped 데이터로 채워진 DataFrame을 만든다.


# -----------------------------------------------------------------------------
# ② Shuffle 단계: 같은 key를 가진 value들을 key별로 그룹화
# -----------------------------------------------------------------------------
# mapped_df: map_phase 결과 DataFrame (columns: key, value)
# 반환: key를 인덱스로, value 리스트를 값으로 갖는 pandas Series
def shuffle(mapped_df):
    return mapped_df.groupby("key")["value"].apply(list)


# -----------------------------------------------------------------------------
# ③ Reduce 단계: 각 key에 대해 value 리스트를 하나의 결과로 합침
# -----------------------------------------------------------------------------
# shuffled: shuffle 결과 Series (index=key, value=리스트)
# reduce_fn: (key, values 리스트)를 받아 최종 값 하나를 반환하는 함수
# 반환: [(key, reduced_value), ...] 리스트
def reduce_phase(shuffled, reduce_fn):
    return [(key, reduce_fn(key, values)) for key, values in shuffled.items()]


# -----------------------------------------------------------------------------
# ④ run_map_reduce: Map → Shuffle → Reduce 파이프라인 실행
# -----------------------------------------------------------------------------
def run_map_reduce(data, map_fn, reduce_fn):
    mapped_df = map_phase(data, map_fn)
    grouped = shuffle(mapped_df)
    return reduce_phase(grouped, reduce_fn)


# -----------------------------------------------------------------------------
# ⑤ Word Count 예제: 문장 리스트에서 단어별 출현 횟수 계산
# -----------------------------------------------------------------------------
def word_count_map(sentence: str) -> list[tuple[str, int]]:
    """문장을 단어로 나누고, 각 단어에 대해 (단어, 1) 쌍을 반환."""
    return [(word.strip().lower(), 1) for word in sentence.split() if word.strip()]


def word_count_reduce(key: str, values: list[int]) -> int:
    """같은 단어에 대한 1들의 리스트를 합쳐 총 출현 횟수로 만듦."""
    return sum(values)


def main() -> None:
    # 예제 입력: 여러 문장
    sentences = [
        "hello world hello",
        "python map reduce",
        "hello python world",
    ]

    result = run_map_reduce(sentences, word_count_map, word_count_reduce)

    print("MapReduce Word Count 결과:")
    print("-" * 30)
    for word, count in sorted(result, key=lambda x: (-x[1], x[0])): # sorted는 오름차순으로 정렬(작은개 먼저), 카운트를 음수로 바꾸어 -3, -2, -1 순으로 작은개 먼저 정렬 되도록 한다.
        print(f"  {word}: {count}")
    print("-" * 30)


if __name__ == "__main__":
    main()

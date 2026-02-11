"""
미션: pandas `DataFrame.insert` 기능을 모방하여 직접 구현하기.

## 원본 pandas 메서드: DataFrame.insert
- **목적**: DataFrame의 특정 위치(loc)에 새로운 컬럼을 "삽입"한다. (기존 컬럼을 뒤로 밀어냄)
- **시그니처(개념)**:
  - `DataFrame.insert(loc, column, value, allow_duplicates=False)`
    - **loc (int)**: 삽입할 컬럼 위치(0-based). 예) 0이면 맨 앞에 삽입
    - **column (label)**: 새 컬럼 이름
    - **value (scalar / array-like / Series 등)**: 새 컬럼 값
      - 스칼라면 모든 행에 브로드캐스트됨
      - 길이가 index 길이와 동일한 array-like면 그대로 매칭
      - Series면 index 정렬(alignment) 규칙이 적용될 수 있음(구현 목표에 따라 단순화 가능)
    - **allow_duplicates (bool)**: False이면 동일한 컬럼명이 이미 존재할 때 에러. True면 중복 컬럼명 허용.
- **리턴**: None (in-place로 DataFrame을 수정)
- **에러/주의 포인트**:
  - allow_duplicates=False & column이 이미 존재하면 ValueError
  - loc가 범위를 벗어나면 IndexError 성격의 예외
  - value 길이 불일치 시 ValueError

## 구현 목표(추천)
- DataFrame을 직접 만들기보다, 학습용으로 "간단한 테이블 구조"를 정의하고
  `insert(loc, column, value, allow_duplicates=False)`를 구현.
- 최소 요구사항:
  - 컬럼 순서 유지/변경(삽입)
  - 스칼라 value 브로드캐스트
  - list/tuple value 길이 검사
  - 중복 컬럼명 처리(allow_duplicates)
"""

from __future__ import annotations

from dataclasses import dataclass
import csv
from pathlib import Path
from typing import Any, Iterable, List, Sequence


@dataclass
class MiniDataFrame:
    """
    pandas.DataFrame을 아주 단순화한 학습용 구조.

    - columns: 컬럼명 순서(중복 가능)
    - rows:    2차원 리스트(행 기반). rows[r][c] 형태로 접근
    """

    columns: List[str]
    rows: List[List[Any]]

    @property
    def nrows(self) -> int:
        return len(self.rows)

    @property
    def ncols(self) -> int:
        return len(self.columns)

    def head(self, n: int = 5) -> "MiniDataFrame":
        return MiniDataFrame(columns=self.columns[:], rows=[r[:] for r in self.rows[:n]])

    def __repr__(self) -> str:
        preview = self.head(5)
        lines = [f"MiniDataFrame(nrows={self.nrows}, ncols={self.ncols})"]
        lines.append("columns=" + repr(preview.columns))
        lines.append("rows=" + repr(preview.rows))
        if self.nrows > 5:
            lines.append("... (more rows)")
        return "\n".join(lines)

    @classmethod
    def from_csv(cls, path: str | Path, *, limit: int | None = None) -> "MiniDataFrame":
        """
        CSV를 읽어서 MiniDataFrame으로 만든다.
        - pandas 없이(csv 모듈로) 읽어서 과제 취지(메서드 모방)에 집중할 수 있게 함.
        - 모든 값은 일단 str로 읽는다(타입 변환은 필요하면 별도 구현).
        """
        p = Path(path)
        with p.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            columns = next(reader)
            rows: List[List[Any]] = []
            for i, row in enumerate(reader):
                rows.append(row)
                if limit is not None and (i + 1) >= limit:
                    break
        return cls(columns=columns, rows=rows)

    def insert(self, loc: int, column: str, value: Any, *, allow_duplicates: bool = False) -> None:
        """
        TODO: pandas DataFrame.insert 모방 구현.

        최소 스펙(권장):
        - 0 <= loc <= len(columns) 범위만 허용. 아니면 IndexError
        - allow_duplicates=False & column이 이미 존재하면 ValueError
        - value:
          - 스칼라면 nrows 길이로 브로드캐스트
          - list/tuple(또는 Sequence)이면 길이가 nrows여야 함. 아니면 ValueError
        - 동작: in-place. 컬럼/모든 row에 loc 위치로 삽입. 반환 None
        """

        # 1) loc 검증
        # TODO: 아래를 구현하세요.
        # if not (0 <= loc <= self.ncols):
        #     raise IndexError(...)
        # - loc는 int만 허용(학습용 단순화). bool은 int의 하위 타입이라 별도로 제외.
        if isinstance(loc, bool) or not isinstance(loc, int):
            raise TypeError(f"loc must be int, got {type(loc).__name__}")

        # - columns가 n개일 때, 삽입 가능한 위치는 0..n (총 n+1개)
        if not (0 <= loc <= self.ncols):
            raise IndexError(f"loc is out of range: {loc} (expected 0 <= loc <= {self.ncols})")

        # 2) 중복 컬럼명 처리
        # TODO: 아래를 구현하세요.
        # if (not allow_duplicates) and (column in self.columns):
        #     raise ValueError(...)
        if (not allow_duplicates) and (column in self.columns):
            raise ValueError(f"column already exists: {column!r}")

        # 3) value를 "각 행에 들어갈 값 리스트"로 정규화
        # TODO: 아래를 구현하세요.
        # col_values = self._normalize_column_values(value)
        col_values = self._normalize_column_values(value)

        # 4) columns / rows 에 실제 삽입
        # TODO: 아래를 구현하세요.
        # self.columns.insert(loc, column)
        # for r, v in zip(self.rows, col_values):
        #     r.insert(loc, v)

        self.columns.insert(loc, column)
        for r, v in zip(self.rows, col_values):
            if len(r) != (self.ncols - 1):
                # (self.columns는 이미 insert 되어 ncols가 1 증가했으므로 -1)
                raise ValueError(
                    f"row length mismatch: expected {self.ncols - 1} before insert, got {len(r)}"
                )
            r.insert(loc, v)

    def _normalize_column_values(self, value: Any) -> List[Any]:
        """
        value를 nrows 길이의 리스트로 만든다.
        - 스칼라면 브로드캐스트
        - Sequence면 길이 검사 후 list로 변환
        """
        # 스칼라 판정(문자열도 Sequence라서 예외 처리)
        is_sequence = isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))

        if self.nrows == 0:
            # 행이 없으면 어떤 value든 "빈 컬럼"으로 해석 가능(단순화)
            return []

        if not is_sequence:
            return [value] * self.nrows

        values_list = list(value)  # type: ignore[arg-type]
        if len(values_list) != self.nrows:
            raise ValueError(f"value length mismatch: expected {self.nrows}, got {len(values_list)}")
        return values_list


if __name__ == "__main__":
    # 실행 예시(과제 테스트용): netflix_titles.csv 앞부분 5행만 로드해서 insert 시도
    data_path = Path(__file__).parent / "data" / "netflix_titles.csv"
    df = MiniDataFrame.from_csv(data_path, limit=5)
    print(df)

    # TODO(구현 후): 아래 코드들이 동작해야 합니다.
    # 1) 스칼라 브로드캐스트 삽입
    df.insert(0, "const", 1)
    print(df.columns[:3], df.rows[0][:3])
    
    # 2) 길이 맞는 리스트 삽입
    df.insert(2, "row_id", [0, 1, 2, 3, 4])
    
    # 3) 중복 컬럼명 처리
    # df.insert(1, "const", 999)               # allow_duplicates=False면 ValueError 기대
    df.insert(1, "const", 999, allow_duplicates=True)  # True면 허용


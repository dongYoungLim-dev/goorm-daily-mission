"""
미션: pandas의 `drop` / `truncate` 기능을 모방하여 직접 구현하기.
파일명이 `drop_truncate.py`이므로, 아래 2개를 함께 다룹니다.

## 1) 원본 pandas 메서드: DataFrame.drop
- **목적**: 지정한 label(행/열)을 제거한다.
- **시그니처(개념)**:
  - `DataFrame.drop(labels=None, axis=0, index=None, columns=None, level=None, inplace=False, errors='raise')`
    - **labels**: 제거할 라벨(단일 또는 리스트)
    - **axis (0 or 1)**: 0이면 행(index), 1이면 열(columns)
    - **index / columns**: axis 대신 명시적으로 행/열 라벨을 지정
    - **inplace (bool)**: True면 원본 수정 후 None 반환
    - **errors {'raise','ignore'}**:
      - raise: 없는 라벨이면 에러
      - ignore: 없는 라벨은 무시
- **리턴**:
  - inplace=False: 삭제 반영된 새로운 DataFrame
  - inplace=True: None

### DataFrame.drop 기능 흐름 생각 정리(검증/보완 반영)
- 축(axis)을 결정한다.
  - axis=0: 행(index) 삭제
  - axis=1: 열(columns) 삭제
  - (또는 index= / columns= 인자를 쓰면 axis 대신 명시적으로 대상 축이 결정됨)
- 삭제 대상 라벨을 정규화한다.
  - 단일 값이면 리스트로 감싼다.
  - 리스트/튜플 등 iterable이면 그대로 리스트로 만든다.
- errors 처리:
  - errors='raise': 없는 라벨이면 예외 발생
  - errors='ignore': 없는 라벨은 무시
- inplace 처리:
  - inplace=True: 원본을 직접 수정하고 None 반환
  - inplace=False: 수정 결과를 반영한 "새 DataFrame"을 만들어 반환
주의: pandas의 drop은 deep copy를 보장하지 않는다.
학습용 구현에서는 inplace=False일 때 컨테이너를 새로 만드는 수준으로 단순화하면 충분하다.

## 2) 원본 pandas 메서드: DataFrame.truncate
- **목적**: "라벨 기준"으로 행/열을 잘라내어(before~after 범위만 남기기) 부분 DataFrame을 만든다.
- **시그니처(개념)**:
  - `DataFrame.truncate(before=None, after=None, axis=None, copy=True)`
    - **before / after**: 남길 구간의 시작/끝 라벨
    - **axis {0,'index',1,'columns'}**: 자를 축(기본은 index)
    - **copy (bool)**: True면 복사본 반환(원본 영향 없음)
- **리턴**: 잘려진 DataFrame
- **주의 포인트**:
  - 정렬된 인덱스/컬럼에서 의미가 명확(구현 목표에 따라 단순화 가능)
  - before/after가 None이면 한쪽만 제한

### DataFrame.truncate 기능 흐름 생각 정리(보완)
- axis를 결정한다.
  - axis=0: 행(index) 기준으로 before~after 범위만 남긴다.
  - axis=1: 열(columns) 기준으로 before~after 범위만 남긴다.
- before/after로 "남길 구간"을 결정한다(양 끝 포함).
  - before=None이면 시작은 맨 앞
  - after=None이면 끝은 맨 뒤
- copy 처리:
  - copy=True이면 새 컨테이너(리스트)를 만들어 반환(원본 영향 최소화)
  - copy=False이면 일부 공유가 가능하지만(학습용에서는 단순화 가능)

## 구현 목표(추천)
- `drop`: axis=0/1, errors='raise'/'ignore', inplace 지원
- `truncate`: axis=0/1, before/after None 처리
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Iterable, List, Sequence


"""
DataFrame.truncate 기능 흐름 생각 정리(보완).

- axis를 결정한다.
  - axis=0: 행(index) 기준으로 before~after 범위만 남긴다.
  - axis=1: 열(columns) 기준으로 before~after 범위만 남긴다.

- before/after를 이용해 "남길 구간"을 결정한다(양 끝 포함).
  - before=None이면 시작은 맨 앞
  - after=None이면 끝은 맨 뒤

- copy 처리:
  - copy=True이면 새 컨테이너(리스트)를 만들어 반환(원본 영향 최소화)
  - copy=False이면 가능한 범위에서 얕게 공유할 수 있으나(학습용에서는 단순화 가능),
    여기서는 이해를 위해 copy=True/False 차이를 최소 구현으로만 반영한다.

주의: pandas는 라벨 기반이고 정렬된 축에서 특히 의미가 명확하다.
학습용 구현에서는 (행: 0..n-1 정수 인덱스, 열: columns 순서) 기준으로 단순화한다.
"""


class MiniDataFrame:
    """
    drop/truncate 구현을 위한 학습용 미니 DataFrame.
    - columns: 컬럼명 순서
    - rows:    2차원 리스트(행 기반). rows[r][c]

    단순화 규칙(중요):
    - "행 라벨(index)"은 0..nrows-1의 정수 위치로 간주한다.
    - "열 라벨(columns)"은 columns의 문자열 라벨로 간주한다.
    """

    def __init__(self, columns: List[str], rows: List[List[Any]]):
        self.columns = columns
        self.rows = rows

    @property
    def nrows(self) -> int:
        return len(self.rows)

    @property
    def ncols(self) -> int:
        return len(self.columns)

    def __repr__(self) -> str:
        preview_rows = self.rows[:3]
        lines = [f"MiniDataFrame(nrows={self.nrows}, ncols={self.ncols})"]
        lines.append("columns=" + repr(self.columns))
        lines.append("rows=" + repr(preview_rows))
        if self.nrows > 3:
            lines.append("... (more rows)")
        return "\n".join(lines)

    @classmethod
    def from_csv(cls, path: str | Path, *, limit: int | None = None) -> "MiniDataFrame":
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

    def drop(
        self,
        labels: Any | None = None,
        *,
        axis: int = 0,
        index: int | Sequence[int] | None = None,
        columns: str | Sequence[str] | None = None,
        inplace: bool = False,
        errors: str = "raise",
    ) -> "MiniDataFrame | None":
        """
        pandas.DataFrame.drop(...)을 학습용으로 단순화해 구현.

        지원 범위:
        - axis=0: 행 삭제(라벨은 int 위치)
        - axis=1: 열 삭제(라벨은 str 컬럼명)
        - index=, columns= 인자 지원
        - errors='raise'/'ignore', inplace 지원
        """
        if errors not in ("raise", "ignore"):
            raise ValueError("errors must be 'raise' or 'ignore'")

        # index/columns가 주어지면 axis 대신 그것을 우선 적용(단순화)
        if index is not None and columns is not None:
            # pandas는 허용하지만, 학습용에서는 명확히 하려고 금지
            raise ValueError("provide only one of index or columns (simplified)")

        if index is not None:
            axis = 0
            labels = index
        elif columns is not None:
            axis = 1
            labels = columns

        if labels is None:
            # 삭제 대상이 없으면 no-op
            return None if inplace else MiniDataFrame(columns=self.columns[:], rows=[r[:] for r in self.rows])

        # labels 정규화
        if isinstance(labels, (list, tuple)):
            targets = list(labels)
        else:
            targets = [labels]

        if axis == 0:
            # 행 삭제: targets는 int여야 한다(학습 단순화)
            drop_idx: set[int] = set()
            for t in targets:
                if isinstance(t, bool) or not isinstance(t, int):
                    raise TypeError("row labels must be int (simplified)")
                if 0 <= t < self.nrows:
                    drop_idx.add(t)
                elif errors == "raise":
                    raise KeyError(t)
            new_rows = [r for i, r in enumerate(self.rows) if i not in drop_idx]
            if inplace:
                self.rows = new_rows
                return None
            return MiniDataFrame(columns=self.columns[:], rows=[r[:] for r in new_rows])

        if axis == 1:
            # 열 삭제: targets는 str이어야 한다(학습 단순화)
            drop_cols: set[int] = set()
            for t in targets:
                if not isinstance(t, str):
                    raise TypeError("column labels must be str (simplified)")
                # 중복 컬럼명까지 고려: 같은 이름인 컬럼은 전부 제거
                matches = [i for i, c in enumerate(self.columns) if c == t]
                if not matches and errors == "raise":
                    raise KeyError(t)
                drop_cols.update(matches)

            new_columns = [c for i, c in enumerate(self.columns) if i not in drop_cols]
            new_rows = [[v for i, v in enumerate(r) if i not in drop_cols] for r in self.rows]
            if inplace:
                self.columns = new_columns
                self.rows = new_rows
                return None
            return MiniDataFrame(columns=new_columns, rows=new_rows)

        raise ValueError("axis must be 0 or 1 (simplified)")

    def truncate(
        self,
        *,
        before: Any | None = None,
        after: Any | None = None,
        axis: int = 0,
        copy: bool = True,
    ) -> "MiniDataFrame":
        """
        pandas.DataFrame.truncate(...)을 학습용으로 단순화해 구현.

        단순화 규칙:
        - axis=0: before/after는 int(행 위치) 또는 None. 범위는 클리핑.
        - axis=1: before/after는 str(컬럼명) 또는 None. 존재하지 않으면 KeyError.
        - 범위는 양 끝 포함(inclusive).
        """
        if axis == 0:
            if before is None:
                start = 0
            else:
                if isinstance(before, bool) or not isinstance(before, int):
                    raise TypeError("before must be int for axis=0 (simplified)")
                start = max(0, before)

            if after is None:
                end = self.nrows - 1
            else:
                if isinstance(after, bool) or not isinstance(after, int):
                    raise TypeError("after must be int for axis=0 (simplified)")
                end = min(self.nrows - 1, after)

            if self.nrows == 0 or start > end:
                return MiniDataFrame(columns=self.columns[:], rows=[])

            selected_rows = self.rows[start : end + 1]
            if copy:
                return MiniDataFrame(columns=self.columns[:], rows=[r[:] for r in selected_rows])
            return MiniDataFrame(columns=self.columns[:], rows=selected_rows)

        if axis == 1:
            if before is None:
                start = 0
            else:
                if not isinstance(before, str):
                    raise TypeError("before must be str for axis=1 (simplified)")
                try:
                    start = self.columns.index(before)
                except ValueError as e:
                    raise KeyError(before) from e

            if after is None:
                end = self.ncols - 1
            else:
                if not isinstance(after, str):
                    raise TypeError("after must be str for axis=1 (simplified)")
                try:
                    end = self.columns.index(after)
                except ValueError as e:
                    raise KeyError(after) from e

            if self.ncols == 0 or start > end:
                return MiniDataFrame(columns=[], rows=[[] for _ in self.rows])

            new_columns = self.columns[start : end + 1]
            # 열 truncate는 슬라이스로 "새 리스트"가 만들어지므로 copy=False라도 완전한 view는 아님(학습 단순화)
            new_rows = [r[start : end + 1] for r in self.rows]
            if copy:
                return MiniDataFrame(columns=new_columns[:], rows=[rr[:] for rr in new_rows])
            return MiniDataFrame(columns=new_columns, rows=new_rows)

        raise ValueError("axis must be 0 or 1 (simplified)")


if __name__ == "__main__":
    data_path = Path(__file__).parent / "data" / "netflix_titles.csv"
    df = MiniDataFrame.from_csv(data_path, limit=5)
    print("original")
    print(df)

    # drop: 열 삭제 테스트
    df2 = df.drop(columns=["director", "NOT_EXIST"], errors="ignore", inplace=False)
    assert df2 is not None
    assert "director" not in df2.columns
    assert df.ncols == 12  # 원본은 그대로

    # truncate: 열 범위 유지 테스트
    df3 = df.truncate(axis=1, before="type", after="country", copy=True)
    assert df3.columns[0] == "type"
    assert df3.columns[-1] == "country"
    assert df3.ncols == (df.columns.index("country") - df.columns.index("type") + 1)

    # truncate: 행 범위 유지 테스트(0..4 중 1..3만)
    df4 = df.truncate(axis=0, before=1, after=3, copy=True)
    assert df4.nrows == 3

    print("\ndrop/truncate tests passed")
"""
미션: pandas `DataFrame.pop` 기능을 모방하여 직접 구현하기.

## 원본 pandas 메서드: DataFrame.pop
- **목적**: 지정한 컬럼을 "꺼내면서(pop)" DataFrame에서 제거한다.
- **시그니처(개념)**:
  - `DataFrame.pop(item)`
    - **item (label)**: 꺼낼 컬럼명
- **리턴**: 꺼낸 컬럼(Series)
- **동작 요약**:
  - `s = df[item]`을 얻고, 동시에 `del df[item]`로 컬럼을 제거한 효과
  - 즉, **in-place로 컬럼이 사라진다**
- **주의 포인트**:
  - 없는 컬럼이면 KeyError 성격의 예외

## 구현 목표(추천)
- `pop(column_name)` 호출 시
  - 해당 컬럼 데이터를 반환
  - 내부 컬럼 목록/데이터에서 해당 컬럼을 제거
"""

from __future__ import annotations

from dataclasses import dataclass
import csv
from pathlib import Path
from typing import Any, List


@dataclass
class MiniSeries:
    """
    pandas.Series를 아주 단순화한 학습용 구조.
    - name: 컬럼명
    - values: 컬럼 값들(행 순서대로)
    """

    name: str
    values: List[Any]

    def __repr__(self) -> str:
        preview = self.values[:5]
        suffix = "" if len(self.values) <= 5 else ", ... (more)"
        return f"MiniSeries(name={self.name!r}, values={preview!r}{suffix})"


@dataclass
class MiniDataFrame:
    """
    pandas.DataFrame을 아주 단순화한 학습용 구조.

    - columns: 컬럼명 순서(중복 가능)
    - rows:    2차원 리스트(행 기반). rows[r][c]
    """

    columns: List[str]
    rows: List[List[Any]]

    @property
    def nrows(self) -> int:
        return len(self.rows)

    @property
    def ncols(self) -> int:
        return len(self.columns)

    def __repr__(self) -> str:
        preview_rows = self.rows[:5]
        lines = [f"MiniDataFrame(nrows={self.nrows}, ncols={self.ncols})"]
        lines.append("columns=" + repr(self.columns))
        lines.append("rows=" + repr(preview_rows))
        if self.nrows > 5:
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

    def pop(self, item: str) -> MiniSeries:
        """
        TODO: pandas.DataFrame.pop(item) 모방 구현.

        핵심 동작:
        - item 컬럼을 **반환하면서**, DataFrame에서 **제거(in-place)** 한다.
        - 없는 컬럼이면 **KeyError**를 발생시킨다.

        단순화 규칙:
        - 중복 컬럼명이 있으면 "가장 왼쪽(처음 등장)" 컬럼을 pop 한다.
        - 반환은 pandas.Series 대신 MiniSeries로 한다.
        """
        # 1) item 컬럼의 인덱스(col_idx) 찾기
        # TODO: 아래를 구현하세요.
        # - self.columns.index(item)을 사용하면 "첫 번째로 등장하는" 컬럼 인덱스를 얻을 수 있음
        # - item이 없으면 ValueError가 나므로, KeyError(item)로 변환해서 던지기
        #
        # try:
        #     col_idx = ...
        # except ValueError as e:
        #     raise KeyError(item) from e

        try:
          col_idx = self.columns.index(item)
        except ValueError as e:
          raise KeyError(item) from e

        # 2) (선택) 데이터 일관성 체크: 각 row 길이가 ncols와 같은지 확인
        # TODO: 아래를 구현하세요.
        # for r in self.rows:
        #     if len(r) != self.ncols:
        #         raise ValueError(...)
        for r in self.rows:
          if len(r) != self.ncols:
            raise ValueError('row length mismatch: expected {self.ncols}, got {len(r)}')
        

        # 3) 각 행에서 해당 컬럼 값을 꺼내서 values 리스트에 모으기 + row에서 제거
        # TODO: 아래를 구현하세요.
        # values: List[Any] = []
        # for r in self.rows:
        #     values.append(r.pop(col_idx))
        values = [r.pop(col_idx)for r in self.rows if len(r) == self.ncols]

        # 4) columns에서도 해당 컬럼명 제거
        # TODO: 아래를 구현하세요.
        # self.columns.pop(col_idx)
        self.columns.pop(col_idx)

        # 5) MiniSeries로 반환
        # TODO: 아래를 구현하세요.
        # return MiniSeries(name=item, values=values)

        return MiniSeries(name=item, values=values)


if __name__ == "__main__":
    data_path = Path(__file__).parent / "data" / "netflix_titles.csv"
    df = MiniDataFrame.from_csv(data_path, limit=5)
    print(df)

    # TODO(구현 후): 아래 테스트를 주석 해제해서 동작 확인
    s = df.pop("title")
    print("popped:", s)
    print("after pop columns:", df.columns)
    
    assert s.name == "title"
    assert len(s.values) == 5
    assert "title" not in df.columns


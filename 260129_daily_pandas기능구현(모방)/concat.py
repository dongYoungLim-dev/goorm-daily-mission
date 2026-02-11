"""
미션: pandas `concat` 기능을 모방하여 직접 구현하기.

## 원본 pandas 함수: pandas.concat
- **목적**: 여러 개의 Series/DataFrame(또는 유사한 테이블 객체)을 축(axis) 방향으로 이어붙인다.
- **시그니처(개념)**:
  - `pd.concat(objs, axis=0, join='outer', ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=False)`
    - **objs**: list/iterable of objects (Series/DataFrame 등)
    - **axis (0 or 1)**:
      - 0: 행 방향으로 붙이기(세로 결합)
      - 1: 열 방향으로 붙이기(가로 결합)
    - **join {'outer','inner'}**:
      - outer: (기본) 합집합 기준으로 맞추고 없는 값은 NaN
      - inner: 교집합 기준으로 맞춤
    - **ignore_index (bool)**: True면 새로운 RangeIndex로 재부여(기존 index 무시)
    - **keys**: 계층형 인덱스(MultiIndex) 레벨을 추가할 때 사용
    - **verify_integrity (bool)**: True면 중복 인덱스가 생기는지 검사(중복이면 에러)
    - **sort (bool)**: 축 라벨(특히 columns) 정렬 여부(버전에 따라 동작 차이 있음)
- **리턴**: 합쳐진 Series 또는 DataFrame
- **주의 포인트**:
  - axis=0에서는 columns 정렬/정합(alignment) 규칙이 핵심
  - axis=1에서는 index 정렬/정합 규칙이 핵심

## 구현 목표(추천)
- 최소 구현(학습용):
  - `concat(objs, axis=0, join='outer', ignore_index=False)` 정도만 구현
  - axis=0: 컬럼을 outer/inner로 맞춘 후 행을 이어붙이기
  - axis=1: 인덱스를 outer/inner로 맞춘 후 열을 이어붙이기
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Iterable, List, Sequence


class MiniDataFrame:
    """
    concat 구현을 위한 학습용 미니 DataFrame.
    - columns: 컬럼명 순서(중복 가능)
    - rows:    2차원 리스트(행 기반). rows[r][c]

    단순화 규칙:
    - 별도 index는 없고, 행 위치(0..nrows-1)를 index로 간주한다.
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


def concat(
    objs: Sequence[MiniDataFrame],
    *,
    axis: int = 0,
    join: str = "outer",
    ignore_index: bool = False,
) -> MiniDataFrame:
    """
    pandas.concat의 핵심 기능을 학습용으로 단순화해 구현.

    지원 범위:
    - axis=0(행 방향), axis=1(열 방향)
    - join='outer'|'inner'
    - ignore_index(학습용 MiniDataFrame에는 별도 index가 없어 axis=0에서 no-op)
    """
    if join not in ("outer", "inner"):
        raise ValueError("join must be 'outer' or 'inner'")
    if axis not in (0, 1):
        raise ValueError("axis must be 0 or 1")
    if len(objs) == 0:
        return MiniDataFrame(columns=[], rows=[])

    # 간단한 데이터 일관성 체크
    for df in objs:
        for r in df.rows:
            if len(r) != df.ncols:
                raise ValueError(f"row length mismatch: expected {df.ncols}, got {len(r)}")

    if axis == 0:
        # columns 정합(alignment)
        if join == "outer":
            out_cols: List[str] = []
            seen: set[str] = set()
            for df in objs:
                for c in df.columns:
                    if c not in seen:
                        seen.add(c)
                        out_cols.append(c)
        else:  # inner
            common: set[str] = set(objs[0].columns)
            for df in objs[1:]:
                common &= set(df.columns)
            # 첫 번째 df의 컬럼 순서 유지
            out_cols = [c for c in objs[0].columns if c in common]

        out_rows: List[List[Any]] = []
        for df in objs:
            col_to_idx = {c: i for i, c in enumerate(df.columns)}
            for r in df.rows:
                new_r: List[Any] = []
                for c in out_cols:
                    if c in col_to_idx:
                        new_r.append(r[col_to_idx[c]])
                    else:
                        new_r.append(None)
                out_rows.append(new_r)

        # ignore_index는 별도 index가 없으므로 의미상 no-op
        return MiniDataFrame(columns=out_cols, rows=out_rows)

    # axis == 1: 행 위치(index) 정합 + columns 이어붙이기
    if join == "outer":
        out_nrows = max(df.nrows for df in objs)
    else:
        out_nrows = min(df.nrows for df in objs)

    out_cols: List[str] = []
    for df in objs:
        # pandas는 axis=1 concat에서 중복 컬럼명을 허용하므로 그대로 append
        out_cols.extend(df.columns)

    out_rows: List[List[Any]] = []
    for i in range(out_nrows):
        row_parts: List[Any] = []
        for df in objs:
            if i < df.nrows:
                row_parts.extend(df.rows[i])
            else:
                row_parts.extend([None] * df.ncols)
        out_rows.append(row_parts)

    return MiniDataFrame(columns=out_cols, rows=out_rows)


if __name__ == "__main__":
    data_path = Path(__file__).parent / "data" / "netflix_titles.csv"
    a = MiniDataFrame.from_csv(data_path, limit=3)
    b = MiniDataFrame.from_csv(data_path, limit=2)

    # axis=0: 세로 결합 (rows 늘어남)
    v = concat([a, b], axis=0, join="outer")
    assert v.nrows == 5
    assert v.ncols == a.ncols

    # axis=1: 가로 결합 (columns 늘어남)
    h = concat([a, b], axis=1, join="inner")
    assert h.nrows == 2
    assert h.ncols == a.ncols + b.ncols

    print("concat tests passed")


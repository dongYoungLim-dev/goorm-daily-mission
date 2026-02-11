"""
미션: pandas `DataFrame.drop_duplicates` 기능을 모방하여 직접 구현하기.

## 원본 pandas 메서드: DataFrame.drop_duplicates
- **목적**: 중복 행(duplicate rows)을 제거한다.
- **시그니처(개념)**:
  - `DataFrame.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)`
    - **subset (label or list-like)**: 중복 판단에 사용할 컬럼들
      - None이면 "모든 컬럼" 기준으로 중복 판단
    - **keep {'first','last', False}**:
      - 'first': 첫 번째만 남기고 나머지 삭제
      - 'last': 마지막만 남기고 나머지 삭제
      - False: 중복되는 것 전부 삭제(유일한 행만 남음)
    - **inplace (bool)**: True면 원본을 수정하고 None 반환
    - **ignore_index (bool)**: True면 결과 인덱스를 0..n-1로 재설정
- **리턴**:
  - inplace=False: 중복 제거된 새로운 DataFrame
  - inplace=True: None
- **주의 포인트**:
  - NaN 비교 규칙(동일 취급 여부) 등 pandas 내부 규칙이 있다. (학습 구현에서는 단순화 가능)
  - subset 컬럼이 존재하지 않으면 KeyError 성격의 예외

## 구현 목표(추천)
- keep 옵션 3가지('first','last',False) 지원
- subset None vs 지정 컬럼 리스트 지원
- ignore_index 지원(선택)
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Iterable, List, Sequence


class MiniDataFrame:
    """
    drop_duplicates 구현을 위한 학습용 미니 DataFrame.
    - columns: 컬럼명 순서
    - rows:    2차원 리스트(행 기반). rows[r][c]
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

    def drop_duplicates(
        self,
        subset: None | str | Sequence[str] = None,
        *,
        keep: str | bool = "first",
        inplace: bool = False,
        ignore_index: bool = False,
    ) -> "MiniDataFrame | None":
        """
        pandas.DataFrame.drop_duplicates(...)를 학습용으로 단순화해 구현.

        지원 범위:
        - subset=None 또는 컬럼명(문자열) 또는 컬럼명 리스트
        - keep='first' | 'last' | False
        - inplace 지원
        - ignore_index는 학습용 MiniDataFrame에는 별도 index가 없어 no-op로 둔다.
        """
        if keep not in ("first", "last", False):
            raise ValueError("keep must be 'first', 'last', or False")

        # subset 정규화 -> 비교에 사용할 컬럼 인덱스 리스트
        if subset is None:
            subset_cols = self.columns
        elif isinstance(subset, str):
            subset_cols = [subset]
        else:
            subset_cols = list(subset)

        subset_idx: List[int] = []
        for c in subset_cols:
            if c not in self.columns:
                raise KeyError(c)
            # 중복 컬럼명은 첫 번째로 등장하는 것을 기준(단순화)
            subset_idx.append(self.columns.index(c))

        def key_for_row(r: List[Any]) -> tuple[Any, ...]:
            return tuple(r[i] for i in subset_idx)

        keys = [key_for_row(r) for r in self.rows]

        if keep == "first":
            seen: set[tuple[Any, ...]] = set()
            keep_mask: List[bool] = []
            for k in keys:
                if k in seen:
                    keep_mask.append(False)
                else:
                    seen.add(k)
                    keep_mask.append(True)
        elif keep == "last":
            last_pos: dict[tuple[Any, ...], int] = {}
            for i, k in enumerate(keys):
                last_pos[k] = i
            keep_mask = [last_pos[k] == i for i, k in enumerate(keys)]
        else:  # keep is False
            counts: dict[tuple[Any, ...], int] = {}
            for k in keys:
                counts[k] = counts.get(k, 0) + 1
            keep_mask = [counts[k] == 1 for k in keys]

        new_rows = [r[:] for r, m in zip(self.rows, keep_mask) if m]

        if inplace:
            self.rows = new_rows
            # ignore_index: 별도 index가 없으므로 처리할 것 없음
            return None

        # ignore_index: 별도 index가 없으므로 처리할 것 없음
        return MiniDataFrame(columns=self.columns[:], rows=new_rows)


if __name__ == "__main__":
    data_path = Path(__file__).parent / "data" / "netflix_titles.csv"
    df = MiniDataFrame.from_csv(data_path, limit=10)

    # 테스트를 위해 0번째 행을 복제해 중복을 인위적으로 만든다.
    df_with_dup = MiniDataFrame(columns=df.columns[:], rows=[r[:] for r in df.rows] + [df.rows[0][:]])
    assert df_with_dup.nrows == 11

    # 1) keep='first'
    out_first = df_with_dup.drop_duplicates(subset=None, keep="first", inplace=False)
    assert out_first is not None
    assert out_first.nrows == 10

    # 2) keep='last' (중복 2개 중 마지막만 남으므로 역시 10)
    out_last = df_with_dup.drop_duplicates(keep="last")
    assert out_last is not None
    assert out_last.nrows == 10

    # 3) keep=False (중복되는 행은 전부 제거되므로 9)
    out_none = df_with_dup.drop_duplicates(keep=False)
    assert out_none is not None
    assert out_none.nrows == 9

    print("drop_duplicates tests passed")


"""
미션: pandas `DataFrame.copy` 기능을 모방하여 직접 구현하기.

## 원본 pandas 메서드: DataFrame.copy
- **목적**: DataFrame을 복사한다. (얕은 복사/깊은 복사 선택 가능)
- **시그니처(개념)**:
  - `DataFrame.copy(deep=True)`
    - **deep (bool)**:
      - True: 데이터와 인덱스/컬럼을 포함해 "깊은 복사"에 가까운 동작
      - False: "얕은 복사" (내부 데이터 버퍼를 공유할 수 있음)
- **리턴**: 복사된 새로운 DataFrame
- **주의 포인트**:
  - pandas에서 deep=True라도 객체(dtype=object) 안의 "파이썬 객체 자체"까지 재귀적으로 deepcopy 하진 않는다.
    (즉, 완전한 의미의 deepcopy와는 차이가 있음)
  - 학습 구현에서는 deep=True면 내부 리스트/배열을 새로 만들고,
    deep=False면 내부 참조를 공유하도록 단순화 가능.

## 구현 목표(추천)
- `copy(deep=True|False)` 지원
- deep=False에서 수정 시 원본에도 영향이 갈 수 있는(공유) 구조를 의도적으로 보여주기
"""

from __future__ import annotations

"""
DataFrame.copy 기능 흐름 생각 정리(수정 반영).

- deep=False(얕은 복사):
  - 신규 DataFrame 객체를 만들되, 내부 데이터(rows 등)는 공유한다.
  - 그래서 복사본을 수정하면 원본에도 영향이 갈 수 있다(학습용으로 의도).

- deep=True(깊은 복사에 가까움):
  - 신규 DataFrame 객체를 만들고 columns/rows 같은 "컨테이너"를 새로 만든다.
  - 단, 원소가 파이썬 객체라면 그 객체 자체까지 재귀적으로 deepcopy 하지는 않는다(= pandas도 동일한 한계가 있음).

깊은 복사 과정(학습용 MiniDataFrame 기준)
1) 복사 대상의 columns와 rows를 가져온다.
2) 새 rows wrapper(list)를 만든다.
3) 각 row를 순회하며 row[:]로 "행 리스트"를 새로 만든다.
4) (선택) columns도 columns[:]로 새 리스트를 만든다.
5) 새 columns/rows로 신규 DataFrame을 만들어 반환한다.
"""

import csv
from pathlib import Path
from typing import Any, List


class MiniDataFrame:
    """
    pandas.DataFrame을 단순화한 학습용 구조.

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

    def copy(self, deep: bool = True) -> "MiniDataFrame":
        """
        pandas.DataFrame.copy(deep=True|False) 모방.

        - deep=True:
          - columns/rows 컨테이너를 새로 만들어 반환(행 리스트까지 복사)
          - 단, 원소가 객체면 객체 자체는 공유될 수 있음(재귀 deepcopy 아님)
        - deep=False:
          - 새 DataFrame 객체는 만들되, columns/rows 컨테이너를 공유(학습 단순화)
        """
        if deep:
            new_columns = self.columns[:] # list slice 를 이용하여 복사본을 new_columns 에 담는다.
            new_rows = [r[:] for r in self.rows] # list comprehension 으로 각 행을 순회 하며 슬라이스를 이용하여 각 행 list를 복사하여 new_rows 에 담는다.
            return MiniDataFrame(columns=new_columns, rows=new_rows)

        # 얕은 복사: 컨테이너(리스트) 참조를 공유
        return MiniDataFrame(columns=self.columns, rows=self.rows)


if __name__ == "__main__":
    data_path = Path(__file__).parent / "data" / "netflix_titles.csv"
    df = MiniDataFrame.from_csv(data_path, limit=5)
    print("original")
    print(df)

    shallow = df.copy(deep=False)
    deep_copied = df.copy(deep=True)

    # 1) 얕은 복사: 내부 데이터 공유 확인
    shallow.rows[0][0] = "CHANGED"
    assert df.rows[0][0] == "CHANGED"

    # 2) 깊은 복사(컨테이너 복사): 내부 데이터 분리 확인
    deep_copied.rows[0][1] = "CHANGED2"
    assert df.rows[0][1] != "CHANGED2"

    print("\ncopy tests passed")

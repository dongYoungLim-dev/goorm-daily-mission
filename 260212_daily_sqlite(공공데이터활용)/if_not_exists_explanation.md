# CREATE TABLE IF NOT EXISTS 설명

## 기본 개념

`CREATE TABLE IF NOT EXISTS`는 SQLite에서 테이블이 이미 존재하는지 확인한 후, 존재하지 않을 때만 테이블을 생성하는 구문입니다.

## 구문 구조

```sql
CREATE TABLE IF NOT EXISTS 테이블명 (
    컬럼1 타입1,
    컬럼2 타입2,
    ...
)
```

## IF NOT EXISTS의 역할

### 1. 에러 방지
- **IF NOT EXISTS 없이**: 테이블이 이미 존재하면 에러 발생
- **IF NOT EXISTS 있으면**: 테이블이 이미 존재해도 에러 없이 무시

### 2. 실행 예시

#### ❌ IF NOT EXISTS 없이 실행 (에러 발생)
```python
# 첫 번째 실행: 성공
cursor.execute("CREATE TABLE bird_tracking (id INTEGER, name TEXT)")

# 두 번째 실행: 에러 발생!
# sqlite3.OperationalError: table bird_tracking already exists
cursor.execute("CREATE TABLE bird_tracking (id INTEGER, name TEXT)")
```

#### ✅ IF NOT EXISTS 있으면 실행 (에러 없음)
```python
# 첫 번째 실행: 테이블 생성 성공
cursor.execute("CREATE TABLE IF NOT EXISTS bird_tracking (id INTEGER, name TEXT)")

# 두 번째 실행: 테이블이 이미 존재하므로 무시 (에러 없음)
cursor.execute("CREATE TABLE IF NOT EXISTS bird_tracking (id INTEGER, name TEXT)")
```

## 사용 시나리오

### 1. 스크립트를 여러 번 실행할 때
```python
# 스크립트를 여러 번 실행해도 안전
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bird_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bird_name TEXT,
        altitude REAL
    )
""")
```

### 2. 데이터베이스 초기화 시
```python
# 데이터베이스가 비어있든, 이미 테이블이 있든 안전하게 실행
def init_database():
    cursor.execute("CREATE TABLE IF NOT EXISTS users (...)")
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (...)")
    cursor.execute("CREATE TABLE IF NOT EXISTS products (...)")
```

### 3. CSV 데이터 로드 시
```python
# CSV 파일을 여러 번 로드해도 테이블 생성 에러 없음
cursor.execute("CREATE TABLE IF NOT EXISTS bird_tracking (...)")
# CSV 데이터 삽입...
```

## 주의사항

### ⚠️ 테이블 구조 변경은 반영되지 않음
```python
# 첫 번째 실행: 테이블 생성 (id, name 컬럼만)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bird_tracking (
        id INTEGER,
        name TEXT
    )
""")

# 두 번째 실행: age 컬럼 추가 시도하지만...
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bird_tracking (
        id INTEGER,
        name TEXT,
        age INTEGER  -- 이 컬럼은 추가되지 않음!
    )
""")
# 결과: 기존 테이블 구조 그대로 유지됨 (age 컬럼 없음)
```

**해결 방법**: 테이블 구조를 변경하려면 `ALTER TABLE` 사용
```python
# 기존 테이블에 컬럼 추가
cursor.execute("ALTER TABLE bird_tracking ADD COLUMN age INTEGER")
```

## 실제 사용 예시

```python
import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# 안전하게 테이블 생성
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bird_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        altitude REAL,
        date_time TEXT,
        bird_name TEXT
    )
""")

# 스크립트를 여러 번 실행해도 에러 없음
conn.commit()
conn.close()
```

## 요약

- ✅ **장점**: 스크립트를 여러 번 실행해도 안전
- ✅ **장점**: 테이블 존재 여부 확인 불필요
- ⚠️ **주의**: 테이블 구조 변경은 반영되지 않음
- 💡 **권장**: 데이터 로드 스크립트에서 자주 사용

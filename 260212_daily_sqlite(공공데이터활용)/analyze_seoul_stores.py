"""
================================================================================
시나리오: 서울 상가(상권) 정보 데이터 분석
================================================================================

[시나리오 설명]
당신은 상권 분석 전문가입니다. 소상공인시장진흥공단에서 제공한 서울 지역 상가(상권) 정보 데이터를
분석하여 서울 지역의 상권 분포, 업종별 특성, 지역별 상권 특성 등을 파악해야 합니다. 이를 통해
상권 활성화 정책 수립, 신규 입점 지역 선정, 상권 경쟁력 분석 등에 활용할 수 있는 인사이트를
도출해야 합니다.

[문제 정의]
1. 지역별 상가 분포 분석
   - 구별 상가 개수 및 밀도 분석
   - 동별 상가 분포 특성
   - 지역별 상권 규모 비교

2. 업종별 분포 분석
   - 대분류/중분류/소분류별 업종 분포
   - 지역별 업종 특성 분석
   - 업종별 집중도 분석 (업종 다양성 지수 등)

3. 상권 경쟁력 분석
   - 지역별 업종 다양성 분석
   - 업종별 경쟁 강도 분석 (동일 업종 밀도)
   - 상권 활성도 지표 개발

4. 입지 특성 분석
   - 도로명 주소 vs 지번 주소 분포
   - 주요 상권 지역 식별
   - 상권 클러스터 분석

5. 업종별 지역 선호도 분석
   - 특정 업종이 집중된 지역 식별
   - 업종별 최적 입지 지역 분석
   - 업종 간 상관관계 분석 (예: 카페와 베이커리, 치킨과 맥주 등)

[분석 힌트]
- CSV 파일을 직접 읽어서 SQLite 데이터베이스에 저장 (csv.reader() 활용)
- SQLite 쿼리만 사용하여 모든 분석 수행:
  * GROUP BY를 활용한 지역별/업종별 집계
  * COUNT(), COUNT(DISTINCT), AVG() 등 집계 함수 활용
  * CASE WHEN을 활용한 조건부 집계 및 분류
  * 서브쿼리를 활용한 복잡한 분석
  * JOIN을 활용한 데이터 결합 (필요시)
  * 윈도우 함수(OVER, PARTITION BY) 활용 가능
- 구/동 정보를 활용한 지역별 그룹화: GROUP BY 시군구명, 행정동명
- 업종 코드(대분류/중분류/소분류)를 활용한 계층적 분석:
  * GROUP BY 상권업종대분류명, 상권업종중분류명, 상권업종소분류명
- 업종 다양성 지수: SQLite 쿼리로 계산
  * COUNT(DISTINCT 업종코드)를 활용한 다양성 측정
  * 서브쿼리로 각 지역의 업종 수 계산
- 상권 클러스터 분석: 위도/경도 기반으로 거리 계산하여 그룹화
- 업종 간 상관관계: 같은 지역(동)에 함께 나타나는 업종 패턴 분석
  * SELF JOIN을 활용하여 동일 지역의 다른 업종 찾기
- 주소 정보 분석: 도로명주소와 지번주소 컬럼 활용
- 결과는 SQLite 쿼리 결과를 print()로 출력하거나 파일로 저장
"""

import sqlite3
import csv
from pathlib import Path

# 데이터 파일 경로
data_path = Path(__file__).parent / 'data' / '소상공인시장진흥공단_상가(상권)정보_서울_202512.csv'

# SQLite 데이터베이스 연결 (현재 파일과 같은 디렉토리에 저장)
db_path = Path(__file__).parent / 'seoul_stores.db'
print(f"데이터베이스 저장 위치: {db_path.absolute()}")
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# CSV 파일을 읽어서 SQLite 데이터베이스에 저장
# 1. 테이블 생성 (CREATE TABLE IF NOT EXISTS 사용)
# 주의: CSV 파일의 모든 컬럼을 포함하여 테이블 생성
create_table_sql = """
CREATE TABLE IF NOT EXISTS stores (
    상가업소번호 TEXT,
    상호명 TEXT,
    지점명 TEXT,
    상권업종대분류코드 TEXT,
    상권업종대분류명 TEXT,
    상권업종중분류코드 TEXT,
    상권업종중분류명 TEXT,
    상권업종소분류코드 TEXT,
    상권업종소분류명 TEXT,
    표준산업분류코드 TEXT,
    표준산업분류명 TEXT,
    시도코드 TEXT,
    시도명 TEXT,
    시군구코드 TEXT,
    시군구명 TEXT,
    행정동코드 TEXT,
    행정동명 TEXT,
    법정동코드 TEXT,
    법정동명 TEXT,
    지번코드 TEXT,
    대지구분코드 TEXT,
    대지구분명 TEXT,
    지번본번지 INTEGER,
    지번부번지 INTEGER,
    지번주소 TEXT,
    도로명코드 TEXT,
    도로명 TEXT,
    건물본번지 INTEGER,
    건물부번지 INTEGER,
    건물관리번호 TEXT,
    건물명 TEXT,
    도로명주소 TEXT,
    구우편번호 TEXT,
    신우편번호 TEXT,
    동정보 TEXT,
    층정보 TEXT,
    호정보 TEXT,
    경도 REAL,
    위도 REAL
)
"""
cursor.execute(create_table_sql)
print("테이블 생성 완료!")

# 기존 데이터가 있으면 삭제 (필요시 주석 해제)
# cursor.execute("DELETE FROM stores")

# 2. CSV 파일 읽기 및 데이터 삽입
with open(data_path, 'r', encoding='utf-8') as f:
    csv_reader = csv.reader(f)
    
    # 첫 번째 줄은 헤더이므로 건너뛰기
    headers = next(csv_reader)
    print(f"컬럼 수: {len(headers)}개")
    
    # 3. 데이터 삽입 (INSERT INTO ... VALUES)
    # 모든 컬럼을 포함하는 INSERT 문
    placeholders = ','.join(['?' for _ in range(len(headers))])
    insert_sql = f"INSERT INTO stores VALUES ({placeholders})"
    
    row_count = 0
    for row in csv_reader:
        try:
            # CSV의 따옴표 제거 및 데이터 정리
            cleaned_row = []
            for value in row:
                # 따옴표 제거
                cleaned_value = value.strip('"') if value else None
                # 빈 문자열은 None으로 변환
                cleaned_value = None if cleaned_value == '' else cleaned_value
                cleaned_row.append(cleaned_value)
            
            # 데이터 타입 변환 (숫자 컬럼)
            final_row = []
            for i, value in enumerate(cleaned_row):
                if value is None:
                    final_row.append(None)
                elif i in [22, 23, 27, 28]:  # 지번본번지, 지번부번지, 건물본번지, 건물부번지
                    try:
                        final_row.append(int(value) if value else None)
                    except ValueError:
                        final_row.append(None)
                elif i in [36, 37]:  # 경도, 위도
                    try:
                        final_row.append(float(value) if value else None)
                    except ValueError:
                        final_row.append(None)
                else:
                    final_row.append(value)
            
            cursor.execute(insert_sql, final_row)
            row_count += 1
            
            # 진행 상황 출력 (1000개마다)
            if row_count % 1000 == 0:
                print(f"진행 중... {row_count}개 행 삽입 완료")
                
        except (ValueError, IndexError) as e:
            print(f"데이터 변환 오류 (행 {row_count + 1}): {e}")
            continue

# 변경사항 저장
conn.commit()
print(f"\n데이터 로드 완료: 총 {row_count}개 행 삽입됨")

# 데이터 확인
cursor.execute("SELECT COUNT(*) FROM stores")
count = cursor.fetchone()[0]
print(f"테이블에 저장된 총 행 수: {count}")

# 샘플 데이터 확인
print("\n샘플 데이터 (상위 3개):")
print("-" * 80)
cursor.execute("SELECT 상호명, 시군구명, 상권업종대분류명, 도로명주소 FROM stores LIMIT 3")
for row in cursor.fetchall():
    print(row)

print("\n" + "=" * 80)
print("서울 상가(상권) 정보 데이터 분석 시작")
print("=" * 80)

# SQLite 쿼리를 사용한 분석 수행
# 기초 수준에 맞춘 간단한 쿼리문

# 1. 지역별 상가 분포 분석
# 설명: 각 구별로 상가가 몇 개 있는지 세어봅니다
print("\n[1] 지역별 상가 분포 분석")
print("-" * 80)
print("설명: 각 구별 상가 개수를 확인합니다")
query1 = """
SELECT 
    시군구명,
    COUNT(*) as 상가수
FROM stores
GROUP BY 시군구명
ORDER BY 상가수 DESC
"""


# 동별 상가 분포 (상위 20개)
# 설명: 각 동별로 상가가 몇 개 있는지 확인합니다
print("\n[1-1] 동별 상가 분포 (상위 20개)")
print("-" * 80)
print("설명: 상가가 많은 동을 확인합니다")
query1_1 = """
SELECT 
    시군구명,
    행정동명,
    COUNT(*) as 상가수
FROM stores
GROUP BY 시군구명, 행정동명
ORDER BY 상가수 DESC
LIMIT 20
"""
# 2. 업종별 분포 분석
# 설명: 어떤 업종의 상가가 가장 많은지 확인합니다
print("\n[2] 업종별 분포 분석")
print("-" * 80)
print("설명: 업종 대분류별 상가 개수를 확인합니다")
query2 = """
SELECT 
    상권업종대분류명,
    COUNT(*) as 상가수
FROM stores
GROUP BY 상권업종대분류명
ORDER BY 상가수 DESC
"""

# 업종 중분류별 분석 (상위 15개)
# 설명: 더 세부적인 업종별 상가 개수를 확인합니다
print("\n[2-1] 업종 중분류별 분포 (상위 15개)")
print("-" * 80)
print("설명: 업종 중분류별 상가 개수를 확인합니다")
query2_1 = """
SELECT 
    상권업종대분류명,
    상권업종중분류명,
    COUNT(*) as 상가수
FROM stores
GROUP BY 상권업종대분류명, 상권업종중분류명
ORDER BY 상가수 DESC
LIMIT 15
"""

# 3. 지역별 업종 다양성 분석
# 설명: 각 구에 몇 가지 종류의 업종이 있는지 확인합니다
print("\n[3] 지역별 업종 다양성 분석")
print("-" * 80)
print("설명: 각 구에 있는 업종의 종류 수를 확인합니다")
query3 = """
SELECT 
    시군구명,
    COUNT(*) as 총상가수,
    COUNT(DISTINCT 상권업종대분류코드) as 업종대분류수,
    COUNT(DISTINCT 상권업종중분류코드) as 업종중분류수
FROM stores
GROUP BY 시군구명
ORDER BY 업종중분류수 DESC
"""

# 4. 주요 상권 지역 식별
# 설명: 상가가 많은 지역을 확인합니다
print("\n[4] 주요 상권 지역 식별 (상위 20개)")
print("-" * 80)
print("설명: 상가가 많은 동을 확인합니다")
query4 = """
SELECT 
    시군구명,
    행정동명,
    COUNT(*) as 상가수
FROM stores
GROUP BY 시군구명, 행정동명
ORDER BY 상가수 DESC
LIMIT 20
"""

# 5. 업종별 지역 분포
# 설명: 각 업종이 어느 구에 많이 있는지 확인합니다
print("\n[5] 업종별 지역 분포 분석")
print("-" * 80)
print("설명: 각 업종이 어느 구에 많이 있는지 확인합니다")

# 음식 업종의 구별 분포
print("\n[5-1] 음식 업종의 구별 분포 (상위 10개)")
query5_1 = """
SELECT 
    시군구명,
    COUNT(*) as 상가수
FROM stores
WHERE 상권업종대분류명 = '음식'
GROUP BY 시군구명
ORDER BY 상가수 DESC
LIMIT 10
"""

# 소매 업종의 구별 분포
print("\n[5-2] 소매 업종의 구별 분포 (상위 10개)")
query5_2 = """
SELECT 
    시군구명,
    COUNT(*) as 상가수
FROM stores
WHERE 상권업종대분류명 = '소매'
GROUP BY 시군구명
ORDER BY 상가수 DESC
LIMIT 10
"""

# 6. 특정 업종이 많은 지역 찾기
# 설명: 특정 업종(예: 카페)이 많은 동을 찾습니다
print("\n[6] 카페가 많은 지역 (상위 10개)")
print("-" * 80)
print("설명: 카페가 많은 동을 확인합니다")
query6 = """
SELECT 
    시군구명,
    행정동명,
    COUNT(*) as 카페수
FROM stores
WHERE 상권업종중분류명 LIKE '%카페%'
GROUP BY 시군구명, 행정동명
ORDER BY 카페수 DESC
LIMIT 10
"""

print("\n" + "=" * 80)
print("서울 상가(상권) 정보 데이터 분석 완료!")
print("=" * 80)

conn.close()

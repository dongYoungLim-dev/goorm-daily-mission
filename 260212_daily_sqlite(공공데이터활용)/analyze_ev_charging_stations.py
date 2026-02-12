"""
================================================================================
시나리오: 전국 전기차 충전소 데이터 분석
================================================================================

[시나리오 설명]
당신은 전기차 인프라 분석 전문가입니다. 정부에서 제공한 전국 전기차 충전소 데이터를 분석하여
전기차 충전 인프라의 현황을 파악하고, 지역별 충전소 분포, 충전 타입별 현황, 운영 시간 분석 등을
통해 전기차 보급 정책 수립에 필요한 인사이트를 도출해야 합니다.

[문제 정의]
1. 지역별 충전소 분포 분석
   - 시도/시군구별 충전소 개수 및 밀도 분석
   - 지역 간 충전소 접근성 비교
   - 충전소 부족 지역 식별

2. 충전 타입별 현황 분석
   - 완속 충전소 vs 급속 충전소 비율
   - 충전 타입별 지역 분포 특성
   - 충전 타입별 운영 시간 패턴 분석

3. 충전소 운영 시간 분석
   - 24시간 운영 충전소 비율
   - 지역별 운영 시간 패턴
   - 충전소 이용 가능 시간대 분석

4. 충전소 접근성 분석
   - 주요 도로/고속도로 인근 충전소 분포
   - 도심 vs 교외 지역 충전소 밀도 비교
   - 충전소 부족 지역 식별

[분석 힌트]
- CSV 파일을 직접 읽어서 SQLite 데이터베이스에 저장 (csv.reader() 활용)
- 데이터 인코딩: 파일이 CP949 또는 EUC-KR 인코딩으로 되어 있을 수 있으므로,
  open() 함수에서 encoding='cp949' 또는 encoding='euc-kr' 옵션 사용 고려
- SQLite 쿼리만 사용하여 모든 분석 수행:
  * GROUP BY를 활용한 지역별/충전타입별 집계
  * COUNT(), AVG(), SUM() 등 집계 함수 활용
  * CASE WHEN을 활용한 조건부 집계
  * 서브쿼리를 활용한 복잡한 분석
  * JOIN을 활용한 데이터 결합 (필요시)
- 시도/시군구 정보를 활용한 지역별 그룹화: GROUP BY 시도, 시군구
- 충전 타입 컬럼을 활용한 분류 분석: GROUP BY 충전타입
- 운영 시간 컬럼을 활용한 시간대별 분석: CASE WHEN으로 시간대 분류
- 위도/경도 컬럼을 활용한 거리 계산: SQLite의 수학 함수 활용
- 결과는 SQLite 쿼리 결과를 print()로 출력하거나 파일로 저장
"""

import sqlite3
import csv
from pathlib import Path

# 데이터 파일 경로
data_path = Path(__file__).parent / 'data' / '180610-전국전기차충전소데이터 (1).csv'

# SQLite 데이터베이스 연결 (현재 파일과 같은 디렉토리에 저장)
db_path = Path(__file__).parent / 'ev_charging_stations.db'
print(f"데이터베이스 저장 위치: {db_path.absolute()}")
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# CSV 파일을 읽어서 SQLite 데이터베이스에 저장
# 1. 테이블 생성 (CREATE TABLE IF NOT EXISTS 사용)
# 주의: CSV 파일의 인코딩이 깨져 보일 수 있으므로, 실제 컬럼명 확인 필요
# 기존 테이블이 있으면 삭제 (컬럼 구조가 변경되었을 수 있으므로)
cursor.execute("DROP TABLE IF EXISTS charging_stations")

create_table_sql = """
CREATE TABLE IF NOT EXISTS charging_stations (
    충전소명 TEXT,
    충전소위치상세 TEXT,
    설치시도명 TEXT,
    휴점일 TEXT,
    이용가능시작시각 TEXT,
    이용가능종료시각 TEXT,
    완속충전가능여부 TEXT,
    급속충전가능여부 TEXT,
    급속충전타입구분 TEXT,
    완속충전기대수 INTEGER,
    급속충전기대수 INTEGER,
    주차료부과여부 TEXT,
    소재지도로명주소 TEXT,
    소재지지번주소 TEXT,
    관리업체명 TEXT,
    관리업체전화번호 TEXT,
    위도 REAL,
    경도 REAL,
    데이터기준일자 TEXT,
    빈컬럼 TEXT
)
"""
cursor.execute(create_table_sql)
print("테이블 생성 완료!")

# 2. CSV 파일 읽기 및 데이터 삽입
# 인코딩 시도: cp949, euc-kr, utf-8 순서로 시도
encodings = ['cp949', 'euc-kr', 'utf-8']
file_opened = False

for encoding in encodings:
    try:
        with open(data_path, 'r', encoding=encoding) as f:
            csv_reader = csv.reader(f)
            
            # 첫 번째 줄은 헤더이므로 건너뛰기
            headers = next(csv_reader)
            print(f"인코딩: {encoding}, 컬럼 수: {len(headers)}개")
            
            # 3. 데이터 삽입 (INSERT INTO ... VALUES)
            # CSV 파일의 컬럼 수에 맞춰 동적으로 생성
            placeholders = ','.join(['?' for _ in range(len(headers))])
            insert_sql = f"INSERT INTO charging_stations VALUES ({placeholders})"
            
            row_count = 0
            for row in csv_reader:
                try:
                    # 데이터 타입 변환
                    final_row = []
                    for i, value in enumerate(row):
                        if value is None or value == '':
                            final_row.append(None)
                        elif i in [9, 10]:  # 완속충전기대수(인덱스 9), 급속충전기대수(인덱스 10)
                            try:
                                final_row.append(int(value) if value else None)
                            except ValueError:
                                final_row.append(None)
                        elif i in [16, 17]:  # 위도(인덱스 16), 경도(인덱스 17)
                            try:
                                final_row.append(float(value) if value else None)
                            except ValueError:
                                final_row.append(None)
                        else:
                            final_row.append(value)
                    
                    # CSV에 20개 컬럼이 있지만 마지막이 빈 컬럼일 수 있으므로 확인
                    if len(final_row) < len(headers):
                        # 부족한 컬럼은 None으로 채움
                        final_row.extend([None] * (len(headers) - len(final_row)))
                    
                    cursor.execute(insert_sql, final_row)
                    row_count += 1
                    
                    # 진행 상황 출력 (100개마다)
                    if row_count % 100 == 0:
                        print(f"진행 중... {row_count}개 행 삽입 완료")
                        
                except (ValueError, IndexError) as e:
                    print(f"데이터 변환 오류 (행 {row_count + 1}): {e}")
                    continue
            
            file_opened = True
            break
            
    except UnicodeDecodeError:
        print(f"인코딩 {encoding} 실패, 다음 인코딩 시도...")
        continue

if not file_opened:
    print("모든 인코딩 시도 실패!")
    conn.close()
    exit(1)

# 변경사항 저장
conn.commit()
print(f"\n데이터 로드 완료: 총 {row_count}개 행 삽입됨")

# 데이터 확인
cursor.execute("SELECT COUNT(*) FROM charging_stations")
count = cursor.fetchone()[0]
print(f"테이블에 저장된 총 행 수: {count}")

# 샘플 데이터 확인
print("\n샘플 데이터 (상위 3개):")
print("-" * 80)
cursor.execute("SELECT 충전소명, 설치시도명, 급속충전가능여부 FROM charging_stations LIMIT 3")
for row in cursor.fetchall():
    print(row)

print("\n" + "=" * 80)
print("전기차 충전소 데이터 분석 시작")
print("=" * 80)

# SQLite 쿼리를 사용한 분석 수행
# 기초 수준에 맞춘 간단한 쿼리문

# 1. 지역별 충전소 분포 분석
# 설명: 각 시도별로 충전소가 몇 개 있는지 세어봅니다
print("\n[1] 지역별 충전소 분포 분석")
print("-" * 80)
print("설명: 각 시도별 충전소 개수를 확인합니다")
query1 = """
SELECT 
    설치시도명,
    COUNT(*) as 충전소수
FROM charging_stations
GROUP BY 설치시도명
ORDER BY 충전소수 DESC
"""
# 2. 급속 충전소 vs 완속 충전소 개수
# 설명: 급속 충전소와 완속 충전소가 각각 몇 개인지 확인합니다
print("\n[2] 충전 타입별 현황 분석")
print("-" * 80)
print("설명: 급속 충전소와 완속 충전소의 개수를 비교합니다")

# 급속 충전소 개수
query2_1 = """
SELECT 
    '급속 충전소' as 타입,
    COUNT(*) as 개수
FROM charging_stations
WHERE 급속충전가능여부 = 'Y'
"""
# 완속 충전소 개수
query2_2 = """
SELECT 
    '완속 충전소' as 타입,
    COUNT(*) as 개수
FROM charging_stations
WHERE 완속충전가능여부 = 'Y'
"""

# 충전기 대수 합계
print("\n충전기 대수 합계:")
query2_3 = """
SELECT 
    SUM(급속충전기대수) as 총급속충전기대수,
    SUM(완속충전기대수) as 총완속충전기대수
FROM charging_stations
"""

# 3. 충전소 운영 시간 분석
# 설명: 24시간 운영하는 충전소가 몇 개인지 확인합니다
print("\n[3] 충전소 운영 시간 분석")
print("-" * 80)
print("설명: 24시간 운영하는 충전소와 시간제한이 있는 충전소를 비교합니다")

query3 = """
SELECT 
    이용가능시작시각,
    이용가능종료시각,
    COUNT(*) as 충전소수
FROM charging_stations
GROUP BY 이용가능시작시각, 이용가능종료시각
ORDER BY 충전소수 DESC
LIMIT 10
"""

# 24시간 운영 충전소 개수
query3_1 = """
SELECT 
    COUNT(*) as 시간24운영충전소수
FROM charging_stations
WHERE 이용가능시작시각 = '00:00' 
  AND (이용가능종료시각 = '00:00' OR 이용가능종료시각 = '23:59' OR 이용가능종료시각 = '24:00')
"""

# 4. 지역별 충전소 상세 정보
# 설명: 각 시도별로 급속/완속 충전소와 충전기 대수를 확인합니다
print("\n[4] 지역별 충전소 상세 정보 (상위 10개)")
print("-" * 80)
print("설명: 시도별로 충전소와 충전기 대수를 확인합니다")

query4 = """
SELECT 
    설치시도명,
    COUNT(*) as 총충전소수,
    SUM(급속충전기대수) as 총급속충전기대수,
    SUM(완속충전기대수) as 총완속충전기대수
FROM charging_stations
GROUP BY 설치시도명
ORDER BY 총충전소수 DESC
LIMIT 10
"""

# 5. 무료 주차 가능한 충전소
# 설명: 주차료가 없는 충전소가 몇 개인지 확인합니다
print("\n[5] 무료 주차 가능한 충전소 분석")
print("-" * 80)
print("설명: 주차료가 없는 충전소의 개수를 확인합니다")

query5 = """
SELECT 
    주차료부과여부,
    COUNT(*) as 충전소수
FROM charging_stations
GROUP BY 주차료부과여부
"""

print("\n" + "=" * 80)
print("전기차 충전소 데이터 분석 완료!")
print("=" * 80)

conn.close()

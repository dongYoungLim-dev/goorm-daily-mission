"""
================================================================================
시나리오: 조류 이동 패턴 데이터 분석
================================================================================

[시나리오 설명]
당신은 조류 생태학 연구원입니다. GPS 추적 장치를 통해 수집된 조류 이동 데이터를 분석하여
조류의 이동 경로, 이동 패턴, 서식지 선호도 등을 파악해야 합니다. 이를 통해 조류 보호 정책 수립,
서식지 보전, 계절별 이동 경로 예측 등에 활용할 수 있는 인사이트를 도출해야 합니다.

[문제 정의]
1. 조류별 이동 경로 분석
   - 각 조류의 이동 경로 시각화
   - 이동 거리 및 속도 분석
   - 이동 방향 패턴 분석

2. 시간대별 이동 패턴 분석
   - 시간대별 이동 활동량 분석
   - 낮/밤 이동 패턴 비교
   - 계절별 이동 패턴 분석

3. 고도별 이동 패턴 분석
   - 고도 분포 분석
   - 이동 시 고도 변화 패턴
   - 서식지별 선호 고도 분석

4. 이동 속도 및 방향 분석
   - 이동 속도 분포 및 통계
   - 방향성 패턴 분석
   - 정지 vs 이동 상태 구분

5. 조류별 특성 비교 분석
   - 조류 종류별 이동 패턴 비교
   - 이동 거리 및 속도 비교
   - 서식지 선호도 비교

[분석 힌트]
- CSV 파일을 직접 읽어서 SQLite 데이터베이스에 저장 (csv.reader() 활용)
- SQLite 쿼리만 사용하여 모든 분석 수행:
  * GROUP BY를 활용한 조류별/시간대별 집계
  * COUNT(), AVG(), MIN(), MAX(), SUM() 등 집계 함수 활용
  * CASE WHEN을 활용한 시간대 분류 (낮/밤, 계절 등)
  * 서브쿼리를 활용한 복잡한 분석
  * 윈도우 함수(OVER, PARTITION BY) 활용 가능
- 날짜/시간 컬럼 분석: SQLite의 datetime 함수 활용 (strftime, date, time 등)
- 고도, 속도, 방향 데이터 분석: AVG(), MIN(), MAX() 등 집계 함수 활용
- 조류 이름(bird_name)을 활용한 종별 그룹화: GROUP BY bird_name
- 이동 거리 계산: SQLite에서 위도/경도 좌표 간 거리 계산 함수 작성
- 이동 상태 분류: CASE WHEN speed_2d < 0.5 THEN '정지' ELSE '이동' END
- 시간대별 분석: strftime('%H', date_time)로 시간 추출 후 GROUP BY
- 계절별 분석: strftime('%m', date_time)로 월 추출 후 CASE WHEN으로 계절 분류
- 결과는 SQLite 쿼리 결과를 print()로 출력하거나 파일로 저장
"""

import sqlite3
import csv
from pathlib import Path

# 데이터 파일 경로
data_path = Path(__file__).parent / 'data' / 'bird_migration.csv'

# SQLite 데이터베이스 연결 (현재 파일과 같은 디렉토리에 저장)
db_path = Path(__file__).parent / '260212_exam.db'
print(f"데이터베이스 저장 위치: {db_path.absolute()}")
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# CSV 파일을 읽어서 SQLite 데이터베이스에 저장
# 1. 테이블 생성 (CREATE TABLE IF NOT EXISTS 사용)
create_table_sql = """
CREATE TABLE IF NOT EXISTS bird_tracking (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  altitude REAL,
  date_time TEXT,
  device_info_serial INTEGER,
  direction REAL,
  latitude REAL,
  longitude REAL,
  speed_2d REAL,
  bird_name TEXT
)
"""

cursor.execute(create_table_sql)
print("테이블 생성 완료!")

# 기존 데이터가 있으면 삭제 (필요시 주석 해제)

# 2. CSV 파일 읽기 및 데이터 삽입
with open(data_path, 'r', encoding='utf-8') as f: 
  csv_reader = csv.reader(f) # 파일을 읽어 가져 온다.

  headers = next(csv_reader)
  print(f"컬럼명 : {headers}")

  insert_sql = """
  INSERT INTO bird_tracking
  (altitude, date_time, device_info_serial, direction, latitude, longitude, speed_2d, bird_name)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  """

  row_count = 0
  for row in csv_reader:
    # CSV 파일의 첫 번째 컬럼은 인덱스이므로 제외하고 실제 데이터만 사용
    if len(row) > 1:
      data = row[1:]  # 첫 번째 컬럼(인덱스) 제외
    else:
      continue  # 데이터가 없으면 건너뛰기

    try: 
      altitude = float(data[0]) if data[0] else None
      date_time = data[1] if data[1] else None
      device_info_serial = int(data[2]) if data[2] else None
      direction = float(data[3]) if data[3] else None
      latitude = float(data[4]) if data[4] else None
      longitude = float(data[5]) if data[5] else None
      speed_2d = float(data[6]) if data[6] else None
      bird_name = data[7] if data[7] else None

      cursor.execute(insert_sql, (
        altitude, date_time, device_info_serial, direction, latitude, longitude, speed_2d, bird_name
      ))

      row_count += 1

      if row_count % 1000 == 0:
        print(f"진행중... {row_count}개 행 삽입 완료")

    except (ValueError, IndexError) as e:
      print(f"데이터 변환 오류 (행 {row_count + 1}): {e}")
      continue


# 변경사항 저장
conn.commit()
print(f"\n데이터 로드 완료: 총 {row_count}개 행 삽입됨")

# 데이터 확인
cursor.execute("SELECT COUNT(*) FROM bird_tracking")
count = cursor.fetchone()[0]
print(f"테이블에 저장된 총 행 수: {count}")

# 샘플 데이터 확인
print("\n샘플 데이터 (상위 5개):")
print("-" * 80)
cursor.execute("SELECT * FROM bird_tracking LIMIT 5")
for row in cursor.fetchall():
    print(row)

print("\n" + "=" * 80)
print("조류 이동 패턴 데이터 분석 시작")
print("=" * 80)

# TODO: SQLite 쿼리를 사용한 분석 수행
# 1. 조류별 이동 경로 분석
query_bird_movement = """
select
  bird_name as 조류명,
  date_time,
  latitude,
  longitude,
  speed_2d as 속도,
  direction as 방향,
  altitude as 고도
from bird_tracking
order by bird_name, date_time;
"""
# 2. 시간대별 이동 패턴 분석
query_time_movement = """
select
  date_time as 시간,
  count(*) as 이동횟수
from bird_tracking
group by date_time
order by date_time;
"""
# 3. 고도별 이동 패턴 분석
query_altitude_movement = """
select
  altitude as 고도,
  count(*) as 이동횟수
from bird_tracking
group by altitude
order by altitude;
"""
# 4. 이동 속도 및 방향 분석
query_speed_direction_movement = """
select
  speed_2d as 속도,
  direction as 방향,
  count(*) as 이동횟수
from bird_tracking
group by speed_2d, direction;
"""
# 5. 조류별 특성 비교 분석
query_bird_comparison = """
select
  bird_name as 조류명,
  count(*) as 이동횟수
from bird_tracking
group by bird_name
order by bird_name;
"""
conn.close()

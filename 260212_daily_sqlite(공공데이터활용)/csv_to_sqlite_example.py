"""
CSV 파일을 읽어서 SQLite 테이블을 만드는 방법 예시
"""

import sqlite3
import csv
from pathlib import Path

# 데이터 파일 경로
data_path = Path('data/bird_migration.csv')

# SQLite 데이터베이스 연결
conn = sqlite3.connect('bird_migration.db')
cursor = conn.cursor()

# 방법 1: CSV 파일의 첫 번째 줄(헤더)을 읽어서 컬럼명 확인 후 테이블 생성
print("=" * 80)
print("CSV 파일을 읽어서 SQLite 테이블 생성하기")
print("=" * 80)

# CSV 파일 열기
with open(data_path, 'r', encoding='utf-8') as f:
    csv_reader = csv.reader(f)
    
    # 첫 번째 줄 읽기 (헤더)
    headers = next(csv_reader)
    print(f"컬럼명: {headers}")
    
    # 테이블 생성 (컬럼 타입 지정)
    # 주의: 첫 번째 컬럼이 빈 문자열이거나 인덱스인 경우 처리 필요
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
    
    # 기존 데이터 삭제 (필요시)
    cursor.execute("DELETE FROM bird_tracking")
    
    # 데이터 삽입
    insert_sql = """
    INSERT INTO bird_tracking 
    (altitude, date_time, device_info_serial, direction, latitude, longitude, speed_2d, bird_name)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    row_count = 0
    for row in csv_reader:
        # 첫 번째 컬럼(인덱스)은 제외하고 나머지 데이터만 사용
        if len(row) > 0 and row[0] == '':  # 첫 번째 컬럼이 빈 경우
            data = row[1:]  # 첫 번째 컬럼 제외
        else:
            data = row
        
        # 데이터 타입 변환 및 None 처리
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
                altitude, date_time, device_info_serial, direction,
                latitude, longitude, speed_2d, bird_name
            ))
            row_count += 1
            
            # 진행 상황 출력 (1000개마다)
            if row_count % 1000 == 0:
                print(f"진행 중... {row_count}개 행 삽입 완료")
                
        except (ValueError, IndexError) as e:
            print(f"데이터 변환 오류 (행 {row_count + 1}): {e}")
            continue

# 변경사항 저장
conn.commit()
print(f"\n총 {row_count}개 행 삽입 완료!")

# 데이터 확인
cursor.execute("SELECT COUNT(*) FROM bird_tracking")
count = cursor.fetchone()[0]
print(f"테이블에 저장된 총 행 수: {count}")

# 샘플 데이터 확인
cursor.execute("SELECT * FROM bird_tracking LIMIT 5")
print("\n샘플 데이터:")
print("-" * 80)
for row in cursor.fetchall():
    print(row)

conn.close()
print("\n작업 완료!")

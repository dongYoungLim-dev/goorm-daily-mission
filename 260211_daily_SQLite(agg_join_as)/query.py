"""
SQLite 학습 쿼리문
- 집계함수 (Aggregate Functions)
- 조인 (Join)
- 컬럼 별명 및 뷰 (Column Aliases and Views)
"""

import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect("/Users/dymacpro/myProject/myDev/My/goorm-ai-study/SQLLite/260211_exam.db")
cursor = conn.cursor()

# ============================================
# 1. 학습 테이블 생성 쿼리문
# ============================================

# 학생 테이블 생성
create_students_table = """
CREATE TABLE IF NOT EXISTS 학생 (
    학생ID INTEGER PRIMARY KEY AUTOINCREMENT,
    이름 TEXT NOT NULL,
    학년 INTEGER,
    학과 TEXT,
    성적 INTEGER
);
"""

# 교수 테이블 생성
create_professors_table = """
CREATE TABLE IF NOT EXISTS 교수 (
    교수ID INTEGER PRIMARY KEY AUTOINCREMENT,
    이름 TEXT NOT NULL,
    학과 TEXT,
    직급 TEXT
);
"""

# 수강 테이블 생성
create_enrollments_table = """
CREATE TABLE IF NOT EXISTS 수강 (
    수강ID INTEGER PRIMARY KEY AUTOINCREMENT,
    학생ID INTEGER,
    교수ID INTEGER,
    과목명 TEXT,
    점수 INTEGER,
    FOREIGN KEY (학생ID) REFERENCES 학생(학생ID),
    FOREIGN KEY (교수ID) REFERENCES 교수(교수ID)
);
"""

# 음반 테이블 생성 (A17 조인 예제용)
create_albums_table = """
CREATE TABLE IF NOT EXISTS 음반 (
    음반ID INTEGER PRIMARY KEY AUTOINCREMENT,
    제목 TEXT NOT NULL,
    아티스트 TEXT,
    발매년도 INTEGER
);
"""

# 노래 테이블 생성
create_songs_table = """
CREATE TABLE IF NOT EXISTS 노래 (
    노래ID INTEGER PRIMARY KEY AUTOINCREMENT,
    제목 TEXT NOT NULL,
    아티스트 TEXT,
    길이 INTEGER
);
"""

# 수록곡 테이블 생성 (조인 예제용)
create_tracks_table = """
CREATE TABLE IF NOT EXISTS 수록곡 (
    수록곡ID INTEGER PRIMARY KEY AUTOINCREMENT,
    음반ID INTEGER,
    노래ID INTEGER,
    순서 INTEGER,
    FOREIGN KEY (음반ID) REFERENCES 음반(음반ID),
    FOREIGN KEY (노래ID) REFERENCES 노래(노래ID)
);
"""

# ============================================
# 2. 샘플 데이터 삽입
# ============================================

# 학생 데이터 삽입
insert_students = """
INSERT INTO 학생 (이름, 학년, 학과, 성적) VALUES
('김철수', 1, '컴퓨터공학', 85),
('이영희', 2, '컴퓨터공학', 92),
('박민수', 1, '전자공학', 78),
('최지영', 3, '컴퓨터공학', 95),
('정수진', 2, '전자공학', 88),
('한동욱', 1, '컴퓨터공학', 82);
"""

# 교수 데이터 삽입
insert_professors = """
INSERT INTO 교수 (이름, 학과, 직급) VALUES
('홍길동', '컴퓨터공학', '교수'),
('김교수', '전자공학', '부교수'),
('이교수', '컴퓨터공학', '조교수');
"""

# 수강 데이터 삽입
insert_enrollments = """
INSERT INTO 수강 (학생ID, 교수ID, 과목명, 점수) VALUES
(1, 1, '데이터베이스', 90),
(1, 1, '알고리즘', 85),
(2, 1, '데이터베이스', 95),
(2, 3, '웹프로그래밍', 92),
(3, 2, '회로이론', 80),
(4, 1, '데이터베이스', 98),
(4, 3, '웹프로그래밍', 95),
(5, 2, '회로이론', 88),
(6, 1, '알고리즘', 82);
"""

# 음반 데이터 삽입
insert_albums = """
INSERT INTO 음반 (제목, 아티스트, 발매년도) VALUES
('Girl''s Day Party #1', 'Girl''s Day', 2012),
('Everyday', 'Girl''s Day', 2013),
('Expectation', 'Girl''s Day', 2013),
('여자대통령', 'Girl''s Day', 2013);
"""

# 노래 데이터 삽입
insert_songs = """
INSERT INTO 노래 (제목, 아티스트, 길이) VALUES
('갸우뚱', 'Girl''s Day', 210),
('Shuppy Shuppy', 'Girl''s Day', 195),
('Control', 'Girl''s Day', 225),
('영러브', 'Girl''s Day', 200),
('한번만 안아줘', 'Girl''s Day', 215),
('반짝반짝', 'Girl''s Day', 190),
('기대해', 'Girl''s Day', 205),
('I Don''t Mind', 'Girl''s Day', 220),
('Easy go', 'Girl''s Day', 195),
('여자대통령', 'Girl''s Day', 240);
"""

# 수록곡 데이터 삽입
insert_tracks = """
INSERT INTO 수록곡 (음반ID, 노래ID, 순서) VALUES
(1, 1, 1),
(1, 2, 2),
(2, 3, 1),
(2, 4, 2),
(3, 5, 1),
(3, 6, 2),
(3, 7, 3),
(4, 8, 1),
(4, 9, 2),
(4, 10, 3);
"""

# ============================================
# 3. 집계함수 (Aggregate Functions)
# ============================================

# COUNT - 레코드 개수 세기
query_count = """
SELECT COUNT(*) AS 총학생수 FROM 학생;
"""

# COUNT with DISTINCT - 중복 제거 후 개수
query_count_distinct = """
SELECT COUNT(DISTINCT 학과) AS 학과수 FROM 학생;
"""

# SUM - 합계
query_sum = """
SELECT SUM(성적) AS 전체성적합계 FROM 학생;
"""

# AVG - 평균 (집계 함수)
# ROUND()는 집계 함수가 아닌 스칼라 함수(수학 함수)입니다.
# 집계 함수: COUNT, SUM, AVG, MAX, MIN 등 (여러 행을 하나의 값으로 집계)
# 스칼라 함수: ROUND, ABS, UPPER, LOWER 등 (단일 값을 변환)
# ROUND(값): 정수로 반올림
# ROUND(값, 소수점자릿수): 지정한 소수점 자릿수까지 반올림 (예: ROUND(값, 2)는 소수점 둘째 자리까지)
query_avg = """
SELECT ROUND(AVG(성적)) AS 평균성적 FROM 학생;
"""

# AVG - 평균 (소수점 첫째 자리까지)
# AVG() 집계 함수의 결과를 ROUND() 스칼라 함수로 반올림
query_avg_decimal = """
SELECT ROUND(AVG(성적), 1) AS 평균성적 FROM 학생;
"""

# MAX - 최대값
query_max = """
SELECT MAX(성적) AS 최고성적 FROM 학생;
"""

# MIN - 최소값
query_min = """
SELECT MIN(성적) AS 최저성적 FROM 학생;
"""

# 여러 집계함수 함께 사용
query_multiple_agg = """
SELECT 
    COUNT(*) AS 학생수,
    ROUND(AVG(성적)) AS 평균성적,
    MAX(성적) AS 최고성적,
    MIN(성적) AS 최저성적,
    SUM(성적) AS 성적합계
FROM 학생;
"""

# 학과별 집계
query_agg_by_dept = """
SELECT 
    학과,
    COUNT(*) AS 학생수,
    ROUND(AVG(성적)) AS 평균성적,
    MAX(성적) AS 최고성적
FROM 학생
GROUP BY 학과;
"""

# ============================================
# 4. 조인 (Join)
# ============================================

# INNER JOIN - 내부 조인
query_inner_join = """
SELECT 
    학생.이름 AS 학생이름,
    수강.과목명,
    수강.점수
FROM 학생
INNER JOIN 수강 ON 학생.학생ID = 수강.학생ID;
"""

# LEFT JOIN - 왼쪽 외부 조인
query_left_join = """
SELECT 
    학생.이름 AS 학생이름,
    수강.과목명,
    수강.점수
FROM 학생
LEFT JOIN 수강 ON 학생.학생ID = 수강.학생ID;
"""

# 세 테이블 조인 (A17 예제)
query_three_table_join = """
SELECT 
    학생.이름 AS 학생이름,
    교수.이름 AS 교수이름,
    수강.과목명,
    수강.점수
FROM 학생
INNER JOIN 수강 ON 학생.학생ID = 수강.학생ID
INNER JOIN 교수 ON 수강.교수ID = 교수.교수ID;
"""

# 음반-수록곡-노래 세 테이블 조인
query_album_track_song_join = """
SELECT 
    음반.제목 AS 음반제목,
    노래.제목 AS 노래제목,
    수록곡.순서
FROM 음반
INNER JOIN 수록곡 ON 음반.음반ID = 수록곡.음반ID
INNER JOIN 노래 ON 수록곡.노래ID = 노래.노래ID
ORDER BY 음반.제목, 수록곡.순서;
"""

# ============================================
# 5. 컬럼 별명 (Column Aliases) - AS 키워드
# ============================================

# 기본 별명 사용
query_alias_basic = """
SELECT 
    이름 AS 학생이름,
    학년 AS 학년수,
    성적 AS 점수
FROM 학생;
"""

# 별명을 사용한 집계함수
query_alias_agg = """
SELECT 
    학과 AS 학과명,
    COUNT(*) AS 인원수,
    ROUND(AVG(성적)) AS 평균점수
FROM 학생
GROUP BY 학과;
"""

# 별명을 사용한 조인
query_alias_join = """
SELECT 
    s.이름 AS 학생이름,
    e.과목명 AS 수강과목,
    e.점수 AS 획득점수
FROM 학생 AS s
INNER JOIN 수강 AS e ON s.학생ID = e.학생ID;
"""

# ============================================
# 6. 뷰 (Views)
# ============================================

# 뷰 생성 - 학생 성적 뷰
create_student_grade_view = """
CREATE VIEW IF NOT EXISTS 학생성적뷰 AS
SELECT 
    학생.학생ID,
    학생.이름 AS 학생이름,
    학생.학과,
    수강.과목명,
    수강.점수
FROM 학생
INNER JOIN 수강 ON 학생.학생ID = 수강.학생ID;
"""

# 뷰 생성 - 학과별 통계 뷰
create_dept_stats_view = """
CREATE VIEW IF NOT EXISTS 학과별통계뷰 AS
SELECT 
    학과,
    COUNT(*) AS 학생수,
    ROUND(AVG(성적)) AS 평균성적,
    MAX(성적) AS 최고성적,
    MIN(성적) AS 최저성적
FROM 학생
GROUP BY 학과;
"""

# 뷰 조회
query_view_select = """
SELECT * FROM 학생성적뷰;
"""

# 뷰를 사용한 쿼리
query_view_usage = """
SELECT 
    학생이름,
    과목명,
    점수
FROM 학생성적뷰
WHERE 점수 >= 90
ORDER BY 점수 DESC;
"""

# 뷰 삭제
drop_view = """
DROP VIEW IF EXISTS 학생성적뷰;
DROP VIEW IF EXISTS 학과별통계뷰;
"""

# ============================================
# 7. 실행 함수
# ============================================

def setup_database():
    """데이터베이스 초기 설정"""
    # 테이블 생성
    cursor.execute(create_students_table)
    cursor.execute(create_professors_table)
    cursor.execute(create_enrollments_table)
    cursor.execute(create_albums_table)
    cursor.execute(create_songs_table)
    cursor.execute(create_tracks_table)
    
    # 뷰 생성
    cursor.execute(create_student_grade_view)
    cursor.execute(create_dept_stats_view)
    
    conn.commit()
    print("테이블 및 뷰 생성 완료!")

def insert_sample_data():
    """샘플 데이터 삽입"""
    cursor.execute(insert_students)
    cursor.execute(insert_professors)
    cursor.execute(insert_enrollments)
    cursor.execute(insert_albums)
    cursor.execute(insert_songs)
    cursor.execute(insert_tracks)
    
    conn.commit()
    print("샘플 데이터 삽입 완료!")

def execute_query(query, description):
    """쿼리 실행 및 결과 출력"""
    print(f"\n{'='*50}")
    print(f"{description}")
    print(f"{'='*50}")
    cursor.execute(query)
    results = cursor.fetchall()
    
    # 컬럼명 가져오기
    columns = [description[0] for description in cursor.description]
    print(f"컬럼: {', '.join(columns)}")
    print("-" * 50)
    
    for row in results:
        print(row)
    
    return results

def main():
    """메인 실행 함수"""
    print("SQLite 학습 쿼리 실행")
    print("="*50)
    
    # 데이터베이스 초기화
    setup_database()
    
    # 샘플 데이터 삽입 (이미 있으면 주석 처리)
    try:
        insert_sample_data()
    except sqlite3.IntegrityError:
        print("이미 데이터가 존재합니다. 건너뜁니다.")
    
    # 집계함수 예제
    print("\n\n[집계함수 예제]")
    execute_query(query_count, "COUNT - 총 학생 수")
    execute_query(query_avg, "AVG - 평균 성적 (정수로 반올림)")
    execute_query(query_avg_decimal, "AVG - 평균 성적 (소수점 첫째 자리까지 반올림)")
    execute_query(query_max, "MAX - 최고 성적")
    execute_query(query_min, "MIN - 최저 성적")
    execute_query(query_sum, "SUM - 성적 합계")
    execute_query(query_multiple_agg, "여러 집계함수 함께 사용")
    execute_query(query_agg_by_dept, "학과별 집계")
    
    # 조인 예제
    print("\n\n[조인 예제]")
    execute_query(query_inner_join, "INNER JOIN - 내부 조인")
    execute_query(query_left_join, "LEFT JOIN - 왼쪽 외부 조인")
    execute_query(query_three_table_join, "세 테이블 조인")
    execute_query(query_album_track_song_join, "음반-수록곡-노래 세 테이블 조인")
    
    # 컬럼 별명 예제
    print("\n\n[컬럼 별명 예제]")
    execute_query(query_alias_basic, "기본 별명 사용")
    execute_query(query_alias_agg, "별명을 사용한 집계함수")
    execute_query(query_alias_join, "별명을 사용한 조인")
    
    # 뷰 예제
    print("\n\n[뷰 예제]")
    execute_query(query_view_select, "뷰 조회")
    execute_query(query_view_usage, "뷰를 사용한 조건 쿼리")
    execute_query("SELECT * FROM 학과별통계뷰;", "학과별 통계 뷰 조회")
    
    # 연결 종료
    conn.close()
    print("\n\n데이터베이스 연결 종료")

if __name__ == "__main__":
    # main()
    setup_database()
    insert_sample_data()

import pandas as pd
import pymysql


'''
sheet2가 삽입이 되지 않아 코드 분리함
'''
# 엑셀 파일 경로
file_path = "영화정보 리스트_2025-05-29.xlsx"

# MySQL 접속 정보
host = 'localhost'
user = 'bmlee77'
password = 'bmlee77'
database = 'dbsubject'
table_name = 'movie_info'

# 시트2만 불러오기
sheet2 = pd.read_excel(file_path, sheet_name="영화정보 리스트_2")

# 컬럼명 지정
sheet2.columns = [
    'moviename', 'movieengname', 'createdate', 'nation',
    'movietype', 'genre', 'moviestate', 'director', 'company'
]

# 공란 NULL 처리
sheet2 = sheet2.where(pd.notnull(sheet2), None)

# DB 연결 및 삽입
conn = pymysql.connect(host=host, user=user, password=password, db=database, charset='utf8mb4')
cursor = conn.cursor()

sql = f"""
INSERT INTO {table_name}
(moviename, movieengname, createdate, nation, movietype, genre, moviestate, director, company)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in sheet2.iterrows():
    cursor.execute(sql, tuple(row))

conn.commit()
cursor.close()
conn.close()

print(f"시트2 데이터만 {len(sheet2)}건 추가 삽입 완료!")

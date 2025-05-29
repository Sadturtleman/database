import pandas as pd
from sqlalchemy import create_engine
import pymysql

# 엑셀 파일 경로
file_path = "영화정보 리스트_2025-05-29.xlsx"

# MySQL 접속 정보
host = 'localhost'
user = 'bmlee77'
password = 'bmlee77'
database = 'dbsubject'
table_name = 'movie_info'

# SQLAlchemy 엔진 생성
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}", echo=False)

# 시트2만 불러오기
sheet2 = pd.read_excel(file_path, sheet_name="영화정보 리스트_2")

# 컬럼 직접 지정 (시트2는 데이터가 바로 시작됨)
sheet2.columns = [
    'moviename',       # 영화명
    'movieengname',    # 영화명(영문)
    'createdate',      # 제작연도
    'nation',          # 제작국가
    'movietype',       # 유형
    'genre',           # 장르
    'moviestate',      # 제작상태
    'director',        # 감독
    'company'          # 제작사
]

# 공란을 NULL로 처리
sheet2 = sheet2.where(pd.notnull(sheet2), None)

# MySQL에 데이터 추가 (append 방식)
sheet2.to_sql(name=table_name, con=engine, if_exists='append', index=False)

print(f"✅ 시트2 데이터만 {len(sheet2)}건 추가 삽입 완료!")

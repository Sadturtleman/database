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

# 엑셀의 모든 시트 불러오기
xls = pd.read_excel(file_path, sheet_name=None)

# 시트 병합
merged = []
for name, sheet in xls.items():
    if sheet.shape[0] < 5:
        continue

    # 컬럼명은 4번째 인덱스(즉 5번째 행)에 있음
    sheet_clean = sheet.iloc[4:].reset_index(drop=True)
    sheet_clean.columns = sheet.iloc[3]  # 컬럼 행 추출
    sheet_clean = sheet_clean.drop(index=0).reset_index(drop=True)

    # 필요한 컬럼만 필터링 (모든 컬럼이 있어야 추가)
    expected_cols = ['영화명', '영화명(영문)', '제작연도', '유형', '장르', '제작상태', '감독', '제작사']
    if not all(col in sheet_clean.columns for col in expected_cols):
        print(f"[스킵됨] '{name}' 시트에서 필요한 컬럼 누락됨")
        continue

    # 필요한 컬럼만 추출
    sheet_filtered = sheet_clean[expected_cols].copy()
    merged.append(sheet_filtered)

# 통합된 데이터프레임 생성
if not merged:
    raise ValueError("유효한 데이터가 포함된 시트가 없습니다.")
df_all = pd.concat(merged, ignore_index=True)

# 공란을 NULL 처리
df_all = df_all.where(pd.notnull(df_all), None)

# 컬럼명 MySQL 스키마에 맞게 변경
df_all.columns = [
    'moviename',       # 영화명
    'movieengname',    # 영화명(영문)
    'createdate',      # 제작연도
    'movietype',       # 유형
    'genre',           # 장르
    'moviestate',      # 제작상태
    'director',        # 감독
    'company'          # 제작사
]

# movieid는 AUTO_INCREMENT이므로 삽입 안함
df_all.to_sql(name=table_name, con=engine, if_exists='append', index=False)

print("MySQL 테이블에 성공적으로 삽입 완료!")

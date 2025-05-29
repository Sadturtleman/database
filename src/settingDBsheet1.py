import pandas as pd
from sqlalchemy import create_engine, text
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

# 엑셀 파일의 모든 시트 불러오기
xls = pd.read_excel(file_path, sheet_name=None)

# 병합용 리스트
merged = []

# 각 시트 처리
for name, sheet in xls.items():
    if sheet.shape[0] < 5:
        continue

    if name == "영화정보 리스트_2":
        # 시트2는 컬럼명이 없고, 데이터가 바로 시작되므로 수동 지정
        sheet.columns = [
            'moviename', 'movieengname', 'createdate',
            'nation', 'movietype', 'genre', 'moviestate',
            'director', 'company'
        ]
        sheet_clean = sheet
    else:
        # 시트1은 5번째 행부터 컬럼 시작
        sheet_clean = sheet.iloc[4:].reset_index(drop=True)
        sheet_clean.columns = sheet.iloc[3]
        sheet_clean = sheet_clean.drop(index=0).reset_index(drop=True)
        sheet_clean.columns = sheet_clean.columns.str.replace(" ", "").str.strip()
        sheet_clean = sheet_clean.rename(columns={
            '제작국가': 'nation'
        })

    expected_cols = ['영화명', '영화명(영문)', '제작연도', 'nation', '유형', '장르', '제작상태', '감독', '제작사']
    if not all(col in sheet_clean.columns for col in expected_cols):
        print(f"[스킵됨] '{name}' 시트에 필수 컬럼 누락됨")
        continue

    sheet_filtered = sheet_clean[expected_cols].copy()
    sheet_filtered.columns = [
        'moviename', 'movieengname', 'createdate', 'nation',
        'movietype', 'genre', 'moviestate', 'director', 'company'
    ]

    merged.append(sheet_filtered)

# 통합 DataFrame 생성
if not merged:
    raise ValueError("유효한 데이터가 포함된 시트가 없습니다.")
df_all = pd.concat(merged, ignore_index=True)

# 공란을 NULL 처리
df_all = df_all.where(pd.notnull(df_all), None)

# 기존 테이블 데이터 삭제
with engine.begin() as conn:
    conn.execute(text(f"DELETE FROM {table_name}"))

# MySQL로 데이터 삽입
df_all.to_sql(name=table_name, con=engine, if_exists='append', index=False)

print(f"✅ 모든 시트 통합 완료! 총 {len(df_all)}건 삽입됨.")

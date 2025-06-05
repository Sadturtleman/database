import pymysql

# DB 연결
conn = pymysql.connect(
    host='ksisem0811-database.duckdns.org',
    user='bmlee77',
    port=3306,
    password='bmlee77',
    database='dbsubject',
    charset='utf8mb4',
    autocommit=True
)
cursor = conn.cursor()

# 기존 데이터 가져오기
cursor.execute("SELECT * FROM movie_info")
rows = cursor.fetchall()

for index, row in enumerate(rows):
    moviename, movieengname, createdate, movietype, genre_str, moviestate, director_str, company_str, nation_str, movieid = row

    # 1. movie 테이블에 INSERT
    cursor.execute("""
        INSERT INTO movie(movie_name, movie_engname, create_year, movie_type, movie_state)
        VALUES (%s, %s, %s, %s, %s)
    """, (moviename, movieengname, createdate, movietype, moviestate))

    # 새로 생성된 mid 가져오기
    mid = cursor.lastrowid

    # 2. genre 테이블에 INSERT
    genres = [g.strip() for g in genre_str.split(',')] if genre_str else []
    for genre in genres:
        cursor.execute("""
            INSERT INTO movie_genre(genre, mid) VALUES (%s, %s)
        """, (genre, mid))

    # 3. nation 테이블 INSERT
    nations = [n.strip() for n in nation_str.split(',')] if nation_str else []
    for nation in nations:
        cursor.execute("""
            INSERT INTO movie_nation(nation, mid) VALUES (%s, %s)
        """, (nation, mid))

    # 4. company 테이블 INSERT
    companies = [c.strip() for c in company_str.split(',')] if company_str else []
    for company in companies:
        cursor.execute("""
            INSERT INTO movie_company(company, mid) VALUES (%s, %s)
        """, (company, mid))

    # 5. 감독 처리 (director + casting)
    directors = [d.strip() for d in director_str.split(',')] if director_str else []
    for dname in directors:
        # 감독 중복 체크
        cursor.execute("SELECT did FROM director WHERE dname = %s", (dname,))
        result = cursor.fetchone()

        if result:
            did = result[0]
        else:
            cursor.execute("INSERT INTO director(dname) VALUES (%s)", (dname,))
            did = cursor.lastrowid

        cursor.execute("INSERT INTO casting(mid, did) VALUES (%s, %s)", (mid, did))

    print(index, row)
print("✅ 정규화 테이블에 데이터 이관 완료!")

cursor.close()
conn.close()

-- movie 테이블 관련 인덱스
CREATE INDEX idx_movie_name ON movie(movie_name);
CREATE INDEX idx_movie_engname ON movie(movie_engname);
CREATE INDEX idx_movie_year ON movie(create_year);

-- movie_nation 테이블 관련 인덱스
CREATE INDEX idx_movie_nation ON movie_nation(nation);

-- director 테이블 관련 인덱스
CREATE INDEX idx_director_name ON director(dname);

-- movie_genre 테이블 관련 인덱스
CREATE INDEX idx_genre ON movie_genre(genre);

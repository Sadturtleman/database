CREATE TABLE `movie_info` (
  `moviename` varchar(255) DEFAULT NULL,
  `movieengname` varchar(255) DEFAULT NULL,
  `createdate` int DEFAULT NULL,
  `movietype` varchar(255) DEFAULT NULL,
  `genre` varchar(255) DEFAULT NULL,
  `moviestate` varchar(255) DEFAULT NULL,
  `director` varchar(255) DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `nation` varchar(100) DEFAULT NULL,
  `movieid` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`movieid`)
) ENGINE=InnoDB AUTO_INCREMENT=65531 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



select * from movie_info;
create table movie(
	mid int auto_increment, 
    movie_name varchar(255),
    movie_engname varchar(255),
    create_year int,
    movie_type varchar(10),
    movie_state varchar(10),
    
    primary key(mid)
);

create table movie_genre(
	mgid int auto_increment,
    genre varchar(255),
    mid int,
    primary key(mgid),
    foreign key(mid) references movie(mid)
    on update cascade
    on delete restrict
);

create table movie_company(
	mcid int auto_increment,
    mid int,
    company varchar(255),
    primary key(mcid),
    foreign key(mid) references movie(mid)
    on update cascade
    on delete restrict
);

create table director(
	did int auto_increment,
    dname varchar(255),
    primary key(did)
);

create table casting(
	cid int auto_increment,
    mid int,
    did int,
    primary key(cid),
    foreign key(mid) references movie(mid)
    on update cascade
    on delete restrict,
    foreign key(did) references director(did)
    on update cascade
    on delete restrict
);
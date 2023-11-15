create table profession
(
    id         int auto_increment
        primary key,
    profession varchar(10) null
);

create table student
(
    id            int auto_increment
        primary key,
    name          varchar(10) null,
    sex           varchar(2)  null,
    age           int         null,
    origin        varchar(10) null,
    profession_id int         null,
    constraint student_profession_id_fk
        foreign key (profession_id) references profession (id)
);

create table user
(
    id       int auto_increment
        primary key,
    username varchar(50) null,
    password varchar(50) null,
    email    varchar(50) null
);

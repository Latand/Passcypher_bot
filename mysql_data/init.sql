CREATE DATABASE IF NOT EXISTS main;
USE main;
create table IF NOT EXISTS users
(
    chat_id  int                                 not null,
    language varchar(4)                          null,
    id       int auto_increment,
    date     timestamp default CURRENT_TIMESTAMP not null,
    google   varchar(1000)                       null,
    enabled  int       default 0                 not null,
    blocked  tinyint   default 0                 null,
    primary key (id, chat_id)
);
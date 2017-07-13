drop database IF EXISTS init;
create database init;


use init;

create table person(
  id INT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  balance DOUBLE PRECISION(20, 4)
);

create table account(
  id INT PRIMARY KEY,
  person_id INT NOT NULL,
  type varchar(255) NOT NULL
)

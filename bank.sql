drop database IF EXISTS init;
create database init;

use init;

drop user IF EXISTS 'user'@'localhost';
flush privileges;

create user 'user'@'localhost' identified by 'password';

create table account(
  `account_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `account_type` varchar(255) NOT NULL,
  `balance` DOUBLE PRECISION(20, 4),
  PRIMARY KEY (id)
);

create table person(
  `person_id` INT AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `account_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_account_id
    FOREIGN KEY (account_id) REFERENCES account (id)
    ON DELETE CASCADE
);

insert into account (account_id, account_type, balance) values (1, "regular", "100");
insert into person (person_id, name, account_id) values (1, "user1", 1);


grant select, insert, update, alter on person to 'user'@'localhost';
grant select, insert, update, alter on account to 'user'@'localhost';

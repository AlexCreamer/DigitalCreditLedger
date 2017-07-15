drop database IF EXISTS init;
create database init;

use init;

drop user IF EXISTS 'user'@'localhost';
flush privileges;

create user 'user'@'localhost' identified by 'password';

create table account(
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `person_id` INT NOT NULL,
  `type` varchar(255) NOT NULL,
  `balance` DOUBLE PRECISION(20, 4),
  PRIMARY KEY (id)
);

create table person(
  `id` INT AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  account_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_account_id
    FOREIGN KEY (account_id) REFERENCES account (id)
    ON DELETE CASCADE
);

grant select, insert, update, alter on person to 'user'@'localhost';
grant select, insert, update, alter on account to 'user'@'localhost';

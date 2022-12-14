
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS Author;
CREATE TABLE Author (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, first_name VARCHAR (32), last_name VARCHAR(128), short_info CHAR(255));

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
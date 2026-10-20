PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE students(id int, name text, age int);
INSERT INTO students VALUES(1,'Ivanov',20);
INSERT INTO students VALUES(2,'Petrov',19);
INSERT INTO students VALUES(3,'Sidorov',21);
COMMIT;

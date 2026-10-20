-- Практична робота 1. Основне завдання: БД myFirstDB.db
-- Запуск (у порожній теці): sqlite3 myFirstDB.db < 01_main_task.sql
CREATE TABLE students(id int, name text, age int);
INSERT INTO students VALUES(1, 'Ivanov', 20);
INSERT INTO students VALUES(2, 'Petrov', 19);
INSERT INTO students VALUES(3, 'Sidorov', 21);
.mode column
.headers on
SELECT * FROM students;
.schema
SELECT * FROM sqlite_master;
-- Резервна копія
.output myDump.sql
.dump
.output stdout
-- Експорт у CSV
.mode csv
.output stud.csv
SELECT * FROM students;
.output stdout
-- Видалення та імпорт
.mode column
DELETE FROM students;
SELECT count(*) AS cnt FROM students;
.import --csv --skip 1 stud.csv students
SELECT * FROM students;
-- Відновлення з резервної копії виконується в оболонці ОС:
--   rm myFirstDB.db && sqlite3 myFirstDB.db < myDump.sql

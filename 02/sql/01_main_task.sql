-- ===================================================================
-- Практична робота 2. Основне завдання
-- Робота зі СКБД SQLite: зміна таблиці, обмеження цілісності
-- (первинний ключ, зовнішній ключ, перевірка), індекси.
-- Запуск:  sqlite3 studentsList.db < 01_main_task.sql
-- ===================================================================

-- --- Рис. 2. Створення таблиці студентів -------------------------
create table students(id int, name text);
.schema students

-- --- Рис. 3. Зміна назви таблиці ---------------------------------
.tables
alter table students rename to stud;
.tables

-- --- Рис. 4. Додавання поля до таблиці ---------------------------
.schema stud
alter table stud add column age int;
.schema stud

-- --- Рис. 5. Обмеження цілісності «первинний ключ» ---------------
drop table stud;
create table students(id INTEGER PRIMARY KEY, name TEXT, age INTEGER);
.schema students

-- --- Рис. 6. Спроба дублювання значення первинного ключа ---------
insert into students(id, name, age) values(1, 'Vasya', 20);
insert into students(id, name, age) values(1, 'Petya', 21);   -- помилка UNIQUE

-- --- Рис. 7. Автоінкрементний сурогатний первинний ключ ----------
drop table students;
create table students(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER);

-- --- Рис. 8-9. Додавання та перегляд даних -----------------------
insert into students(name, age) values('Petya', 21);
insert into students(name, age) values('Vasya', 20);
.headers on
.mode column
select * from students;

-- --- Рис. 10-14. Таблиця «студентські групи» ---------------------
create table groups(id integer primary key autoincrement, number text, starosta text);
.tables
.schema groups
insert into groups(number, starosta) values(201, 'Ivanov');
insert into groups(number, starosta) values(202, 'Petrova');
select * from groups;

-- --- Рис. 15-16. Складений первинний ключ ------------------------
CREATE TABLE passport(seria TEXT, number TEXT, who_gave TEXT, PRIMARY KEY(seria, number));
insert into passport values('EO', '123432', 'Mykolaiv');
insert into passport values('EK', '123432', 'Odesa');
insert into passport values('EK', '123432', 'Kiev');          -- помилка UNIQUE

-- --- Рис. 17. Обмеження цілісності «зовнішній ключ» --------------
alter table students add column group_id references groups(id);
.schema students

-- --- Рис. 18-20. Порушення посилальної цілісності ----------------
update students set group_id = 3;      -- проходить: контроль FK вимкнено
select * from students;
select * from groups;

-- --- Рис. 21-23. Увімкнення контролю посилальної цілісності ------
pragma foreign_keys;
pragma foreign_keys = on;
pragma foreign_keys;
update students set group_id = 3;      -- тепер помилка FOREIGN KEY

-- --- Рис. 24-25. Усунення порушення ------------------------------
update students set group_id = 1 where id = 1;
update students set group_id = 2 where id = 2;
select * from students;

-- --- Рис. 26-28. Зовнішній ключ на етапі створення таблиці -------
drop table students;
CREATE TABLE students(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  group_id INTEGER,
  FOREIGN KEY(group_id) REFERENCES groups(id)
);
.schema students

-- --- Рис. 30-33. Обмеження цілісності «перевірка» ----------------
alter table students add column age INTEGER CHECK(age>0 and age<150);
.schema students
insert into students(name, age, group_id) values('Vasya', 20, 1);
insert into students(name, age, group_id) values('Petya', 220, 1);  -- помилка CHECK
insert into students(name, age, group_id) values('Klya', -2, 2);    -- помилка CHECK
select * from students;

-- --- Рис. 34-36. Створення індексів ------------------------------
create index stud_age on students(age);
create unique index stud_name on students(name);
.indices students
select * from sqlite_master where type='index';

-- --- Рис. 37. Перевірка роботи унікального індексу ---------------
insert into students(name, age, group_id) values('Petya', 19, 2);
insert into students(name, age, group_id) values('Petya', 20, 1);   -- помилка UNIQUE

-- --- Рис. 38-41. Складений унікальний індекс ---------------------
drop index stud_name;
select * from sqlite_master where type='index';
create unique index stud_name on students(group_id, name);
select * from sqlite_master where type='index';

-- --- Рис. 42-44. Тестування складеного індексу -------------------
select * from students;
insert into students(name, age, group_id) values('Petya', 20, 2);   -- помилка UNIQUE
insert into students(name, age, group_id) values('Petya', 20, 1);   -- успішно
select * from students;

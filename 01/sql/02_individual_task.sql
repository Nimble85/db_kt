-- Практична робота 1. Індивідуальне завдання: БД library.db (бібліотека)
-- Запуск (у порожній теці): sqlite3 library.db < 02_individual_task.sql
PRAGMA foreign_keys = ON;

CREATE TABLE authors(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  full_name TEXT NOT NULL,
  country TEXT
);

CREATE TABLE books(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  author_id INTEGER,
  year INTEGER,
  pages INTEGER,
  FOREIGN KEY(author_id) REFERENCES authors(id)
);

-- Наповнення (10 авторів, 12 книг)
INSERT INTO authors(full_name, country) VALUES('Taras Shevchenko', 'Ukraine');
INSERT INTO authors(full_name, country) VALUES('Lesya Ukrainka', 'Ukraine');
INSERT INTO authors(full_name, country) VALUES('Ivan Franko', 'Ukraine');
INSERT INTO authors(full_name, country) VALUES('Mykhailo Kotsiubynskyi', 'Ukraine');
INSERT INTO authors(full_name, country) VALUES('George Orwell', 'United Kingdom');
INSERT INTO authors(full_name, country) VALUES('Ray Bradbury', 'USA');
INSERT INTO authors(full_name, country) VALUES('Stanislaw Lem', 'Poland');
INSERT INTO authors(full_name, country) VALUES('Franz Kafka', 'Czech Republic');
INSERT INTO authors(full_name, country) VALUES('Haruki Murakami', 'Japan');
INSERT INTO authors(full_name, country) VALUES('Isaac Asimov', 'USA');
INSERT INTO books(title, author_id, year, pages) VALUES('Kobzar', 1, 1840, 320);
INSERT INTO books(title, author_id, year, pages) VALUES('Lisova pisnia', 2, 1911, 128);
INSERT INTO books(title, author_id, year, pages) VALUES('Zakhar Berkut', 3, 1883, 256);
INSERT INTO books(title, author_id, year, pages) VALUES('Tini zabutykh predkiv', 4, 1911, 144);
INSERT INTO books(title, author_id, year, pages) VALUES('1984', 5, 1949, 328);
INSERT INTO books(title, author_id, year, pages) VALUES('Animal Farm', 5, 1945, 112);
INSERT INTO books(title, author_id, year, pages) VALUES('Fahrenheit 451', 6, 1953, 256);
INSERT INTO books(title, author_id, year, pages) VALUES('Solaris', 7, 1961, 204);
INSERT INTO books(title, author_id, year, pages) VALUES('The Trial', 8, 1925, 255);
INSERT INTO books(title, author_id, year, pages) VALUES('Norwegian Wood', 9, 1987, 296);
INSERT INTO books(title, author_id, year, pages) VALUES('Kafka on the Shore', 9, 2002, 505);
INSERT INTO books(title, author_id, year, pages) VALUES('The Castle', 8, 1926, 352);

-- Видалення записів (автор 1 має книги, видалення дало б помилку FK; тут його не видаляємо)
DELETE FROM books WHERE id = 12;
DELETE FROM authors WHERE id = 10;

-- Експорт у CSV
PRAGMA foreign_keys = ON;
.headers on
.mode csv
.output authors.csv
SELECT * FROM authors;
.output books.csv
SELECT * FROM books;
.output stdout

-- Резервна копія
.output library_dump.sql
.dump
.output stdout
.backup library_backup.db

-- Очищення та імпорт з CSV
DELETE FROM books;
DELETE FROM authors;
.import --csv --skip 1 authors.csv authors
.import --csv --skip 1 books.csv books
.mode column
SELECT count(*) AS authors FROM authors;
SELECT count(*) AS books FROM books;

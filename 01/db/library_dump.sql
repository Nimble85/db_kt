PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE authors(
id INTEGER PRIMARY KEY AUTOINCREMENT,
full_name TEXT NOT NULL,
country TEXT
);
INSERT INTO authors VALUES(1,'Taras Shevchenko','Ukraine');
INSERT INTO authors VALUES(2,'Lesya Ukrainka','Ukraine');
INSERT INTO authors VALUES(3,'Ivan Franko','Ukraine');
INSERT INTO authors VALUES(4,'Mykhailo Kotsiubynskyi','Ukraine');
INSERT INTO authors VALUES(5,'George Orwell','United Kingdom');
INSERT INTO authors VALUES(6,'Ray Bradbury','USA');
INSERT INTO authors VALUES(7,'Stanislaw Lem','Poland');
INSERT INTO authors VALUES(8,'Franz Kafka','Czech Republic');
INSERT INTO authors VALUES(9,'Haruki Murakami','Japan');
CREATE TABLE books(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
author_id INTEGER,
year INTEGER,
pages INTEGER,
FOREIGN KEY(author_id) REFERENCES authors(id)
);
INSERT INTO books VALUES(1,'Kobzar',1,1840,320);
INSERT INTO books VALUES(2,'Lisova pisnia',2,1911,128);
INSERT INTO books VALUES(3,'Zakhar Berkut',3,1883,256);
INSERT INTO books VALUES(4,'Tini zabutykh predkiv',4,1911,144);
INSERT INTO books VALUES(5,'1984',5,1949,328);
INSERT INTO books VALUES(6,'Animal Farm',5,1945,112);
INSERT INTO books VALUES(7,'Fahrenheit 451',6,1953,256);
INSERT INTO books VALUES(8,'Solaris',7,1961,204);
INSERT INTO books VALUES(9,'The Trial',8,1925,255);
INSERT INTO books VALUES(10,'Norwegian Wood',9,1987,296);
INSERT INTO books VALUES(11,'Kafka on the Shore',9,2002,505);
INSERT INTO sqlite_sequence VALUES('authors',10);
INSERT INTO sqlite_sequence VALUES('books',12);
COMMIT;

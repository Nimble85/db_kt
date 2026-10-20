#!/usr/bin/env python3
"""
Індивідуальне завдання практичної роботи 1: окрема БД library.db
(предметна область «бібліотека»): дві таблиці з первинними ключами,
по 10+ записів, видалення записів, експорт у CSV, резервне копіювання, відновлення.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_session import run, save, shell

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE, "db")
DB = "library.db"

AUTHORS = [("Taras Shevchenko", "Ukraine"), ("Lesya Ukrainka", "Ukraine"),
           ("Ivan Franko", "Ukraine"), ("Mykhailo Kotsiubynskyi", "Ukraine"),
           ("George Orwell", "United Kingdom"), ("Ray Bradbury", "USA"),
           ("Stanislaw Lem", "Poland"), ("Franz Kafka", "Czech Republic"),
           ("Haruki Murakami", "Japan"), ("Isaac Asimov", "USA")]
BOOKS = [("Kobzar", 1, 1840, 320), ("Lisova pisnia", 2, 1911, 128),
         ("Zakhar Berkut", 3, 1883, 256), ("Tini zabutykh predkiv", 4, 1911, 144),
         ("1984", 5, 1949, 328), ("Animal Farm", 5, 1945, 112),
         ("Fahrenheit 451", 6, 1953, 256), ("Solaris", 7, 1961, 204),
         ("The Trial", 8, 1925, 255), ("Norwegian Wood", 9, 1987, 296),
         ("Kafka on the Shore", 9, 2002, 505), ("The Castle", 8, 1926, 352)]

STEPS = [
    ("ind02", ["pragma foreign_keys = on;", "pragma foreign_keys;"]),
    ("ind03", [["CREATE TABLE authors(",
                "id INTEGER PRIMARY KEY AUTOINCREMENT,",
                "full_name TEXT NOT NULL,",
                "country TEXT",
                ");"]]),
    ("ind04", [["CREATE TABLE books(",
                "id INTEGER PRIMARY KEY AUTOINCREMENT,",
                "title TEXT NOT NULL,",
                "author_id INTEGER,",
                "year INTEGER,",
                "pages INTEGER,",
                "FOREIGN KEY(author_id) REFERENCES authors(id)",
                ");"]]),
    ("ind05", [".tables", ".schema"]),
    ("ind06", [".headers on", ".mode column"]
              + ["insert into authors(full_name, country) values('%s', '%s');" % a for a in AUTHORS]
              + ["select * from authors;"]),
    ("ind07", ["insert into books(title, author_id, year, pages) values('%s', %d, %d, %d);" % b for b in BOOKS]
              + ["select * from books;"]),
    ("ind08", ["insert into authors(id, full_name, country) values(1, 'Duplicate Author', 'Nowhere');"]),
    ("ind09", ["insert into books(title, author_id, year, pages) values('Unknown', 99, 2000, 100);"]),
    ("ind10", ["delete from books where id = 12;",
               "delete from authors where id = 10;",
               "delete from authors where id = 1;",
               "select count(*) as authors from authors;",
               "select count(*) as books from books;"]),
    ("ind11", [".mode csv", ".output authors.csv", "select * from authors;",
               ".output books.csv", "select * from books;", ".output stdout",
               ".shell cat authors.csv", ".shell cat books.csv"]),
    ("ind12", [".output library_dump.sql", ".dump", ".output stdout",
               ".backup library_backup.db", ".shell ls -l library_dump.sql library_backup.db"]),
    ("ind13", [".mode column", "delete from books;", "delete from authors;",
               "select count(*) as authors from authors;",
               "select count(*) as books from books;"]),
    ("ind14", [".import --csv --skip 1 authors.csv authors",
               ".import --csv --skip 1 books.csv books",
               "select count(*) as authors from authors;",
               "select count(*) as books from books;",
               "select b.id, b.title, a.full_name from books b join authors a on a.id = b.author_id order by b.id;"]),
]


def main():
    os.makedirs(DB_DIR, exist_ok=True)
    for f in (DB, "authors.csv", "books.csv", "library_dump.sql",
              "library_backup.db", "library_restored.db"):
        p = os.path.join(DB_DIR, f)
        if os.path.exists(p):
            os.remove(p)
    res = run([DB], DB_DIR, STEPS, banner_name="ind01")
    res["ind15"] = shell(DB_DIR, [
        "sqlite3 library_restored.db < library_dump.sql",
        "sqlite3 -header -column library_restored.db \"select count(*) as authors from authors; select count(*) as books from books;\"",
        "sqlite3 library_backup.db \"select count(*) as books_in_backup from books;\""])
    save("ind", res)
    print("Збережено %d логів" % len(res))


if __name__ == "__main__":
    main()

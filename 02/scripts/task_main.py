#!/usr/bin/env python3
"""
Основне завдання практичної роботи 2: сеанс роботи з БД studentsList.db.
Кроки повністю повторюють рис. 1-34 методичних вказівок.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_session import run, save

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE, "db")
DB = "studentsList.db"

STEPS = [
    ("fig02", ["create table students(id int, name text);",
               ".schema students"]),
    ("fig03", [".tables",
               "alter table students rename to stud;",
               ".tables"]),
    ("fig04", [".schema stud",
               "alter table stud add column age int;",
               ".schema stud"]),
    ("fig05", ["drop table stud;",
               "create table students(id INTEGER PRIMARY KEY, name TEXT, age INTEGER);",
               ".schema students"]),
    ("fig06", ["insert into students(id, name, age) values(1, 'Vasya', 20);",
               "insert into students(id, name, age) values(1, 'Petya', 21);"]),
    ("fig07", ["drop table students;",
               "create table students(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER);"]),
    ("fig08", ["insert into students(name, age) values('Petya', 21);",
               "insert into students(name, age) values('Vasya', 20);"]),
    ("fig09", [".headers on", ".mode column", "select * from students;"]),
    ("fig10", ["create table groups(id integer primary key autoincrement, number text, starosta text);"]),
    ("fig11", [".tables"]),
    ("fig12", [".schema groups"]),
    ("fig13", ["insert into groups(number, starosta) values(201, 'Ivanov');",
               "insert into groups(number, starosta) values(202, 'Petrova');"]),
    ("fig14", ["select * from groups;"]),
    ("fig15", ["CREATE TABLE passport(seria TEXT, number TEXT, who_gave TEXT, PRIMARY KEY(seria, number));"]),
    ("fig16", ["insert into passport values('EO', '123432', 'Mykolaiv');",
               "insert into passport values('EK', '123432', 'Odesa');",
               "insert into passport values('EK', '123432', 'Kiev');"]),
    ("fig17", ["alter table students add column group_id references groups(id);",
               ".schema students"]),
    ("fig18", ["update students set group_id = 3;"]),
    ("fig19", ["select * from students;"]),
    ("fig20", ["select * from groups;"]),
    ("fig21", ["pragma foreign_keys;"]),
    ("fig22", ["pragma foreign_keys = on;", "pragma foreign_keys;"]),
    ("fig23", ["update students set group_id = 3;"]),
    ("fig24", ["update students set group_id = 1 where id = 1;",
               "update students set group_id = 2 where id = 2;"]),
    ("fig25", ["select * from students;"]),
    ("fig26", ["drop table students;"]),
    ("fig27", [["CREATE TABLE students(",
                "id INTEGER PRIMARY KEY AUTOINCREMENT,",
                "name TEXT,",
                "group_id INTEGER,",
                "FOREIGN KEY(group_id) REFERENCES groups(id)",
                ");"]]),
    ("fig28", [".schema students"]),
    ("fig30", ["alter table students add column age INTEGER CHECK(age>0 and age<150);"]),
    ("fig31", [".schema students"]),
    ("fig32", [["insert into students(name, age, group_id)", "values('Vasya', 20, 1);"],
               ["insert into students(name, age, group_id)", "values('Petya', 220, 1);"],
               ["insert into students(name, age, group_id)", "values('Klya', -2, 2);"]]),
    ("fig33", ["select * from students;"]),
    ("fig34a", ["create index stud_age on students(age);",
                "create unique index stud_name on students(name);"]),
    ("fig35", [".indices students"]),
    ("fig36", ["select * from sqlite_master where type='index';"]),
    ("fig37", [["insert into students(name, age, group_id)", "values('Petya', 19, 2);"],
               ["insert into students(name, age, group_id)", "values('Petya', 20, 1);"]]),
    ("fig38", ["drop index stud_name;"]),
    ("fig39", ["select * from sqlite_master where type='index';"]),
    ("fig40", ["create unique index stud_name on students(group_id, name);"]),
    ("fig41", ["select * from sqlite_master where type='index';"]),
    ("fig42", ["select * from students;"]),
    ("fig43", [["insert into students(name, age, group_id)", "values('Petya', 20, 2);"]]),
    ("fig44", [["insert into students(name, age, group_id)", "values('Petya', 20, 1);"],
               "select * from students;"]),
]


def main():
    os.makedirs(DB_DIR, exist_ok=True)
    path = os.path.join(DB_DIR, DB)
    if os.path.exists(path):
        os.remove(path)          # чистий запуск сеансу
    res = run(DB, DB_DIR, STEPS,
              prompt_line=("fig01", "c:\\temp\\sqlite>sqlite3 " + DB))
    save("main", res)
    print("\nЗбережено %d логів у %s" % (len(res), os.path.join(BASE, "logs")))


if __name__ == "__main__":
    main()

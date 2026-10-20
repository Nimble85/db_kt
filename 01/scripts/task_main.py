#!/usr/bin/env python3
"""
Основне завдання практичної роботи 1: сеанси роботи з БД myFirstDB.db.
Кроки відповідають рис. 1-22 методичних вказівок (macOS: оболонка замість cmd).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_session import run, save, shell

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE, "db")
DB = "myFirstDB.db"


def main():
    os.makedirs(DB_DIR, exist_ok=True)
    for f in (DB, "myDump.sql", "myDump2.sql", "stud.csv"):
        p = os.path.join(DB_DIR, f)
        if os.path.exists(p):
            os.remove(p)
    res = {}

    # Рис. 1-2: підготовка середовища (macOS)
    res["fig01"] = shell(DB_DIR, ["which sqlite3", "sqlite3 --version"])
    res["fig02"] = shell(DB_DIR, ["cd ../db && pwd", "ls"])

    # Рис. 3: запуск sqlite3 без БД, .help (початок виводу)
    r = run([], DB_DIR, [("fig03", [".help"])], banner_name="fig03_banner")
    b = r["fig03_banner"].rstrip("\n ")
    if b.endswith("sqlite>"):
        b = b[:-len("sqlite>")].rstrip("\n ")
    lines = (b + "\n" + r["fig03"]).split("\n")
    res["fig03"] = "\n".join(lines[:26])

    # Рис. 4-12: створення БД, таблиця, дамп
    steps = [
        ("fig06", [".databases"]),
        ("fig07", ["create table students(id int, name text, age int);",
                   "insert into students values(1, 'Ivanov', 20);",
                   "insert into students values(2, 'Petrov', 19);",
                   "insert into students values(3, 'Sidorov', 21);"]),
        ("fig08", [".mode column", ".headers on"]),
        ("fig09", ["select * from students;"]),
        ("fig10", [".schema"]),
        ("fig11", ["select * from sqlite_master;"]),
        ("fig12", [".output myDump.sql", ".dump", ".output stdout"]),
    ]
    r = run([DB], DB_DIR, steps, banner_name="fig04")
    res.update(r)

    # Рис. 13-15: вміст дампу, дамп з оболонки, відновлення
    res["fig13"] = shell(DB_DIR, ["cat myDump.sql"])
    res["fig14"] = shell(DB_DIR, ["sqlite3 myFirstDB.db .dump > myDump2.sql",
                                  "cat myDump2.sql", "diff myDump.sql myDump2.sql && echo 'файли ідентичні'"])
    res["fig15"] = shell(DB_DIR, ["rm myFirstDB.db", "ls", "sqlite3 myFirstDB.db < myDump.sql", "ls"])

    # Рис. 16-22: підключення до відновленої БД, експорт/імпорт CSV
    steps = [
        ("fig17", [".tables"]),
        ("fig18", [".mode column", ".headers on", "select * from students;"]),
        ("fig19", [".mode csv", ".output stud.csv", "select * from students;",
                   ".output stdout", ".shell cat stud.csv"]),
        ("fig20", [".mode column", "delete from students;",
                   "select * from students;", "select count(*) as cnt from students;"]),
        ("fig21", [".import --csv --skip 1 stud.csv students",
                   "select count(*) as cnt from students;"]),
        ("fig22", ["select * from students;"]),
    ]
    r = run([DB], DB_DIR, steps, banner_name="fig16")
    res.update(r)
    save("main", res)
    print("Збережено %d логів" % len(res))


if __name__ == "__main__":
    main()

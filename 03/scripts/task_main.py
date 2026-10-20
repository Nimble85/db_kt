#!/usr/bin/env python3
"""
Основне завдання практичної роботи 3: запити на вибірку даних до БД food.db.
Кроки повторюють рис. 1-32 методичних вказівок.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_session import run, save

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE, "db")
DB = "food.db"

STEPS = [
    ("fig02", [".tables"]),
    ("fig03", [".schema"]),
    ("fig07", [".headers on", ".mode column", "select * from food_types;"]),
    ("fig08", ["select name from food_types;"]),
    ("fig09", ["select name from episodes;"], 10),
    ("fig10", ["select name from episodes LIMIT 5;"]),
    ("fig11", ["select * from foods limit 5;"]),
    ("fig12", [".width 3 3 30", "select * from foods limit 5;"]),
    ("fig13", [".width auto", "select * from episodes where season = 2;"]),
    ("fig14", ["select * from foods where type_id = 2 or type_id = 3;"], 10),
    ("fig15", ["select * from foods where type_id in (2,3);"], 10),
    ("fig16", ["select * from foods where name like '%carrot%';"]),
    ("fig17", ["select * from episodes where season = 3 and name like '%boyfriend%';"]),
    ("fig18", ["select count(*) from episodes;"]),
    ("fig19", ["select count(*) from episodes where season = 2;"]),
    ("fig20", ["select count(distinct season) from episodes;"]),
    ("fig21", [["select season, count(id)", "from episodes", "group by season;"]]),
    ("fig22", [["select season", "from episodes", "group by season", "having count(id) > 20;"]]),
    ("fig23", ["select name from food_types order by name;"]),
    ("fig24", ["select * from foods where type_id = 1 order by name desc;"], 12),
    ("fig25", ["select * from episodes order by season, name desc;"], 12),
    ("fig26", [["select season, count(id)", "from episodes", "group by season",
                "order by 2 desc;"]]),
    ("fig27", [["select f.name, t.name", "from foods f inner join food_types t",
                "on f.type_id = t.id", "limit 10;"]]),
    ("fig28", [["select f.name", "from foods f inner join food_types t",
                "on f.type_id = t.id",
                "where f.name like '%salad%' and t.name = 'Vegetables';"]]),
    ("fig29", [["select e.name, count(f.food_id)", "from episodes e inner join foods_episodes f",
                "on e.id = f.episode_id", "group by e.name", "order by 2 desc", "limit 5;"]]),
    ("fig30", [["select e.season, count(distinct f.food_id)",
                "from episodes e inner join foods_episodes f",
                "on e.id = f.episode_id", "group by e.season", "order by 2 desc", "limit 3;"]]),
    ("fig31", [["select e.season, count(distinct e.id)",
                "from episodes e inner join foods_episodes fe",
                "on e.id = fe.episode_id", "inner join foods f on fe.food_id = f.id",
                "where f.name like '%Ice Cream%'", "group by e.season;"]]),
    ("fig32", [["select distinct e.*", "from episodes e inner join foods_episodes fe",
                "on e.id = fe.episode_id", "inner join foods f on fe.food_id = f.id",
                "inner join food_types t on f.type_id = t.id",
                "where t.name = 'Bakery' and e.season = 5;"]]),
]


def restore(dbname):
    """Відновлення БД із дампу foods.sql (рис. 1)."""
    path = os.path.join(DB_DIR, dbname)
    if os.path.exists(path):
        os.remove(path)
    with open(os.path.join(BASE, "sql", "foods.sql")) as f:
        subprocess.run(["sqlite3", dbname], cwd=DB_DIR, stdin=f, check=True)


def main():
    os.makedirs(DB_DIR, exist_ok=True)
    restore(DB)
    res = run(DB, DB_DIR, STEPS,
              prompt_line=("fig01", "$ sqlite3 food.db < foods.sql\n$ sqlite3 " + DB))
    save("main", res)
    print("\nЗбережено %d логів" % len(res))


if __name__ == "__main__":
    main()

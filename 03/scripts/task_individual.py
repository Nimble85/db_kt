#!/usr/bin/env python3
"""Індивідуальне завдання практичної роботи 3: 7 запитів до БД «Страви» (food_ind.db)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_session import run, save
from task_main import restore, DB_DIR

DB = "food_ind.db"

STEPS = [
    ("ind01", [".headers on", ".mode column",
               "select * from food_types where name like 'D%';"]),
    ("ind02", ["select * from foods where type_id between 3 and 5;"], 12),
    ("ind03", ["select * from episodes where season = 9 and name like '%fin%';"]),
    ("ind04", [["select t.name, count(f.id) as foods_count",
                "from food_types t left join foods f on f.type_id = t.id",
                "group by t.id, t.name;"]]),
    ("ind05", [["select t.name, count(f.id) as foods_count",
                "from food_types t inner join foods f on f.type_id = t.id",
                "group by t.id, t.name", "order by foods_count desc", "limit 3;"]]),
    ("ind06", [["select f.name, count(distinct fe.episode_id) as episodes_count",
                "from foods f inner join foods_episodes fe on fe.food_id = f.id",
                "group by f.id, f.name", "order by episodes_count desc", "limit 1;"]]),
    ("ind07", [["select e.season, count(distinct f.type_id) as types_count",
                "from episodes e inner join foods_episodes fe on fe.episode_id = e.id",
                "inner join foods f on f.id = fe.food_id",
                "group by e.season", "order by e.season;"]]),
]


def main():
    restore(DB)
    res = run(DB, DB_DIR, STEPS, prompt_line=("ind00", "$ sqlite3 " + DB))
    res.pop("ind00")
    save("ind", res)
    print("\nЗбережено %d логів" % len(res))


if __name__ == "__main__":
    main()

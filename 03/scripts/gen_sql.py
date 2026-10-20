#!/usr/bin/env python3
"""Формує sql/01_main_task.sql та sql/02_individual_task.sql зі сценаріїв task_*.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import task_main
import task_individual

SQL = os.path.join(task_main.BASE, "sql")


def write(fname, title, db, steps, prefix, label):
    out = ["-- ===================================================================",
           "-- Практична робота 3. " + title,
           "-- Запуск у порожній теці: sqlite3 %s < ../sql/foods.sql  (відновлення БД)" % db,
           "--                         sqlite3 %s < ../sql/%s" % (db, fname),
           "-- ===================================================================",
           "", ".headers on", ".mode column", ""]
    for st in steps:
        name, cmds = st[0], st[1]
        out.append("-- --- %s %s ---" % (label, name))
        for c in cmds:
            if isinstance(c, (list, tuple)):
                out.append("\n".join(c))
            elif c in (".headers on", ".mode column"):
                continue
            else:
                out.append(c)
        out.append("")
    with open(os.path.join(SQL, fname), "w") as f:
        f.write("\n".join(out))


write("01_main_task.sql", "Основне завдання: запити на вибірку даних", "food.db",
      task_main.STEPS, "main", "Рис.")
write("02_individual_task.sql", "Індивідуальне завдання: запити до БД «Страви»",
      "food_ind.db", task_individual.STEPS, "ind", "Запит")
print("sql згенеровано")

#!/usr/bin/env python3
"""
Індивідуальне завдання практичної роботи 2.

Окрема БД shop.db: дві таблиці (categories, products) з обмеженнями цілісності
первинного ключа в кожній, зовнішнього ключа в products, перевірок (CHECK)
та двома індексами, один з яких унікальний.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_session import run, save

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE, "db")
DB = "shop.db"

STEPS = [
    # Створення таблиць із обмеженнями цілісності
    ("ind02", ["pragma foreign_keys = on;", "pragma foreign_keys;"]),
    ("ind03", [["CREATE TABLE categories(",
                "id INTEGER PRIMARY KEY AUTOINCREMENT,",
                "name TEXT NOT NULL,",
                "margin REAL CHECK(margin >= 0 AND margin <= 100)",
                ");"]]),
    ("ind04", [["CREATE TABLE products(",
                "id INTEGER PRIMARY KEY AUTOINCREMENT,",
                "sku TEXT NOT NULL,",
                "name TEXT NOT NULL,",
                "price REAL CHECK(price > 0),",
                "qty INTEGER CHECK(qty >= 0),",
                "category_id INTEGER,",
                "FOREIGN KEY(category_id) REFERENCES categories(id)",
                ");"]]),
    ("ind05", [".tables", ".schema"]),
    # Наповнення даними
    ("ind06", [".headers on", ".mode column",
               "insert into categories(name, margin) values('Noutbuky', 15);",
               "insert into categories(name, margin) values('Smartfony', 20);",
               "insert into categories(name, margin) values('Aksesuary', 35);",
               "select * from categories;"]),
    ("ind07", ["insert into products(sku, name, price, qty, category_id) values('NB-1001', 'Lenovo IdeaPad', 24999.00, 7, 1);",
               "insert into products(sku, name, price, qty, category_id) values('SM-2001', 'Samsung A55', 16499.50, 12, 2);",
               "insert into products(sku, name, price, qty, category_id) values('AC-3001', 'Mysha Logitech', 749.00, 40, 3);",
               "select * from products;"]),
    # Перевірка первинного ключа
    ("ind08", ["insert into categories(id, name, margin) values(1, 'Planshety', 18);"]),
    # Перевірка обмеження CHECK
    ("ind09", ["insert into products(sku, name, price, qty, category_id) values('NB-1002', 'HP Pavilion', -100, 5, 1);",
               "insert into products(sku, name, price, qty, category_id) values('NB-1003', 'Acer Aspire', 21000, -3, 1);",
               "insert into categories(name, margin) values('Monitory', 150);"]),
    # Перевірка зовнішнього ключа
    ("ind10", ["insert into products(sku, name, price, qty, category_id) values('XX-9001', 'Nevidoma kategoriya', 500, 1, 99);",
               "delete from categories where id = 1;"]),
    # Індекси
    ("ind11", ["create unique index idx_products_sku on products(sku);",
               "create index idx_products_name on products(name);"]),
    ("ind12", [".indices products",
               "select type, name, tbl_name, sql from sqlite_master where type='index';"]),
    # Перевірка роботи унікального індексу
    ("ind13", ["insert into products(sku, name, price, qty, category_id) values('SM-2001', 'Samsung A56', 18999, 4, 2);",
               "insert into products(sku, name, price, qty, category_id) values('SM-2002', 'Samsung A56', 18999, 4, 2);",
               "select * from products;"]),
    # Використання індексів оптимізатором
    ("ind14", ["explain query plan select * from products where sku = 'SM-2002';",
               "explain query plan select * from products where name = 'Samsung A56';"]),
    # Підсумкова вибірка зі з'єднанням таблиць
    ("ind15", [["select p.id, p.sku, p.name, p.price, c.name as category",
                "from products p join categories c on c.id = p.category_id",
                "order by c.name, p.name;"]]),
]


def main():
    os.makedirs(DB_DIR, exist_ok=True)
    path = os.path.join(DB_DIR, DB)
    if os.path.exists(path):
        os.remove(path)
    res = run(DB, DB_DIR, STEPS,
              prompt_line=("ind01", "c:\\temp\\sqlite>sqlite3 " + DB))
    save("ind", res)
    print("\nЗбережено %d логів" % len(res))


if __name__ == "__main__":
    main()

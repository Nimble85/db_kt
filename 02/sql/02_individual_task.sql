-- ===================================================================
-- Практична робота 2. Індивідуальне завдання
-- Окрема БД інтернет-магазину: дві таблиці з первинними ключами,
-- зовнішній ключ, обмеження-перевірки та два індекси (один унікальний).
-- Запуск:  sqlite3 shop.db < 02_individual_task.sql
-- ===================================================================

pragma foreign_keys = on;
pragma foreign_keys;

-- --- Таблиця категорій товарів -----------------------------------
CREATE TABLE categories(
  id INTEGER PRIMARY KEY AUTOINCREMENT,            -- первинний ключ
  name TEXT NOT NULL,
  margin REAL CHECK(margin >= 0 AND margin <= 100) -- перевірка націнки, %
);

-- --- Таблиця товарів ---------------------------------------------
CREATE TABLE products(
  id INTEGER PRIMARY KEY AUTOINCREMENT,            -- первинний ключ
  sku TEXT NOT NULL,
  name TEXT NOT NULL,
  price REAL CHECK(price > 0),                     -- перевірка ціни
  qty INTEGER CHECK(qty >= 0),                     -- перевірка залишку
  category_id INTEGER,
  FOREIGN KEY(category_id) REFERENCES categories(id)  -- зовнішній ключ
);

.tables
.schema

-- --- Наповнення даними -------------------------------------------
.headers on
.mode column
insert into categories(name, margin) values('Noutbuky', 15);
insert into categories(name, margin) values('Smartfony', 20);
insert into categories(name, margin) values('Aksesuary', 35);
select * from categories;

insert into products(sku, name, price, qty, category_id) values('NB-1001', 'Lenovo IdeaPad', 24999.00, 7, 1);
insert into products(sku, name, price, qty, category_id) values('SM-2001', 'Samsung A55', 16499.50, 12, 2);
insert into products(sku, name, price, qty, category_id) values('AC-3001', 'Mysha Logitech', 749.00, 40, 3);
select * from products;

-- --- Перевірка обмеження первинного ключа ------------------------
insert into categories(id, name, margin) values(1, 'Planshety', 18);   -- помилка UNIQUE

-- --- Перевірка обмежень CHECK ------------------------------------
insert into products(sku, name, price, qty, category_id) values('NB-1002', 'HP Pavilion', -100, 5, 1);
insert into products(sku, name, price, qty, category_id) values('NB-1003', 'Acer Aspire', 21000, -3, 1);
insert into categories(name, margin) values('Monitory', 150);

-- --- Перевірка зовнішнього ключа ---------------------------------
insert into products(sku, name, price, qty, category_id) values('XX-9001', 'Nevidoma kategoriya', 500, 1, 99);
delete from categories where id = 1;   -- заборонено: на категорію є посилання

-- --- Індекси ------------------------------------------------------
create unique index idx_products_sku on products(sku);   -- унікальний
create index idx_products_name on products(name);        -- неунікальний
.indices products
select type, name, tbl_name, sql from sqlite_master where type='index';

-- --- Перевірка роботи унікального індексу ------------------------
insert into products(sku, name, price, qty, category_id) values('SM-2001', 'Samsung A56', 18999, 4, 2);  -- помилка
insert into products(sku, name, price, qty, category_id) values('SM-2002', 'Samsung A56', 18999, 4, 2);  -- успішно
select * from products;

-- --- Використання індексів оптимізатором -------------------------
explain query plan select * from products where sku = 'SM-2002';
explain query plan select * from products where name = 'Samsung A56';

-- --- Підсумкова вибірка зі з'єднанням таблиць --------------------
select p.id, p.sku, p.name, p.price, c.name as category
from products p join categories c on c.id = p.category_id
order by c.name, p.name;

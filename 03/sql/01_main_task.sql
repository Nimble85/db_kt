-- ===================================================================
-- Практична робота 3. Основне завдання: запити на вибірку даних
-- Запуск у порожній теці: sqlite3 food.db < ../sql/foods.sql  (відновлення БД)
--                         sqlite3 food.db < ../sql/01_main_task.sql
-- ===================================================================

.headers on
.mode column

-- --- Рис. fig02 ---
.tables

-- --- Рис. fig03 ---
.schema

-- --- Рис. fig07 ---
select * from food_types;

-- --- Рис. fig08 ---
select name from food_types;

-- --- Рис. fig09 ---
select name from episodes;

-- --- Рис. fig10 ---
select name from episodes LIMIT 5;

-- --- Рис. fig11 ---
select * from foods limit 5;

-- --- Рис. fig12 ---
.width 3 3 30
select * from foods limit 5;

-- --- Рис. fig13 ---
.width auto
select * from episodes where season = 2;

-- --- Рис. fig14 ---
select * from foods where type_id = 2 or type_id = 3;

-- --- Рис. fig15 ---
select * from foods where type_id in (2,3);

-- --- Рис. fig16 ---
select * from foods where name like '%carrot%';

-- --- Рис. fig17 ---
select * from episodes where season = 3 and name like '%boyfriend%';

-- --- Рис. fig18 ---
select count(*) from episodes;

-- --- Рис. fig19 ---
select count(*) from episodes where season = 2;

-- --- Рис. fig20 ---
select count(distinct season) from episodes;

-- --- Рис. fig21 ---
select season, count(id)
from episodes
group by season;

-- --- Рис. fig22 ---
select season
from episodes
group by season
having count(id) > 20;

-- --- Рис. fig23 ---
select name from food_types order by name;

-- --- Рис. fig24 ---
select * from foods where type_id = 1 order by name desc;

-- --- Рис. fig25 ---
select * from episodes order by season, name desc;

-- --- Рис. fig26 ---
select season, count(id)
from episodes
group by season
order by 2 desc;

-- --- Рис. fig27 ---
select f.name, t.name
from foods f inner join food_types t
on f.type_id = t.id
limit 10;

-- --- Рис. fig28 ---
select f.name
from foods f inner join food_types t
on f.type_id = t.id
where f.name like '%salad%' and t.name = 'Vegetables';

-- --- Рис. fig29 ---
select e.name, count(f.food_id)
from episodes e inner join foods_episodes f
on e.id = f.episode_id
group by e.name
order by 2 desc
limit 5;

-- --- Рис. fig30 ---
select e.season, count(distinct f.food_id)
from episodes e inner join foods_episodes f
on e.id = f.episode_id
group by e.season
order by 2 desc
limit 3;

-- --- Рис. fig31 ---
select e.season, count(distinct e.id)
from episodes e inner join foods_episodes fe
on e.id = fe.episode_id
inner join foods f on fe.food_id = f.id
where f.name like '%Ice Cream%'
group by e.season;

-- --- Рис. fig32 ---
select distinct e.*
from episodes e inner join foods_episodes fe
on e.id = fe.episode_id
inner join foods f on fe.food_id = f.id
inner join food_types t on f.type_id = t.id
where t.name = 'Bakery' and e.season = 5;

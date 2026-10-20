-- ===================================================================
-- Практична робота 3. Індивідуальне завдання: запити до БД «Страви»
-- Запуск у порожній теці: sqlite3 food_ind.db < ../sql/foods.sql  (відновлення БД)
--                         sqlite3 food_ind.db < ../sql/02_individual_task.sql
-- ===================================================================

.headers on
.mode column

-- --- Запит ind01 ---
select * from food_types where name like 'D%';

-- --- Запит ind02 ---
select * from foods where type_id between 3 and 5;

-- --- Запит ind03 ---
select * from episodes where season = 9 and name like '%fin%';

-- --- Запит ind04 ---
select t.name, count(f.id) as foods_count
from food_types t left join foods f on f.type_id = t.id
group by t.id, t.name;

-- --- Запит ind05 ---
select t.name, count(f.id) as foods_count
from food_types t inner join foods f on f.type_id = t.id
group by t.id, t.name
order by foods_count desc
limit 3;

-- --- Запит ind06 ---
select f.name, count(distinct fe.episode_id) as episodes_count
from foods f inner join foods_episodes fe on fe.food_id = f.id
group by f.id, f.name
order by episodes_count desc
limit 1;

-- --- Запит ind07 ---
select e.season, count(distinct f.type_id) as types_count
from episodes e inner join foods_episodes fe on fe.episode_id = e.id
inner join foods f on f.id = fe.food_id
group by e.season
order by e.season;

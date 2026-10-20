#!/bin/sh
# Перевірка: відновлення БД із дампу та прогін фінальних .sql на чистих БД у тимчасовій теці.
set -e
W=$(cd "$(dirname "$0")/.." && pwd); T=$(mktemp -d); cd "$T"
sqlite3 a.db < "$W/sql/foods.sql"
[ "$(sqlite3 a.db 'select count(*) from foods')" = 413 ] && [ "$(sqlite3 a.db 'select count(*) from episodes')" = 181 ] && echo "restore: OK (413/181)"
sqlite3 a.db < "$W/sql/01_main_task.sql" >/dev/null && echo "main: OK"
sqlite3 a.db < "$W/sql/02_individual_task.sql" | grep -q "Hot Dog" && echo "individual: OK (Hot Dog)"
rm -rf "$T"

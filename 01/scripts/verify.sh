#!/bin/sh
# Перевірка: прогін фінальних .sql на чистих БД у тимчасовій теці.
set -e
W=$(cd "$(dirname "$0")/.." && pwd); T=$(mktemp -d); cd "$T"
sqlite3 main.db < "$W/sql/01_main_task.sql" >/dev/null
sqlite3 main.db "select count(*) from students" | grep -qx 3 && echo "main: OK (3 рядки)"
rm main.db; sqlite3 main.db < myDump.sql; sqlite3 main.db "select count(*) from students" | grep -qx 3 && echo "restore main: OK"
sqlite3 lib.db < "$W/sql/02_individual_task.sql" >/dev/null
[ "$(sqlite3 lib.db 'select count(*) from authors')" = 9 ] && [ "$(sqlite3 lib.db 'select count(*) from books')" = 11 ] && echo "individual: OK (9/11)"
sqlite3 r.db < library_dump.sql; [ "$(sqlite3 r.db 'select count(*) from books')" = 11 ] && echo "restore individual: OK"
if sqlite3 lib.db "pragma foreign_keys=on; insert into authors(id,full_name) values(1,'x');" 2>&1 | grep -q UNIQUE; then echo "PK error: OK"; fi
if sqlite3 lib.db "pragma foreign_keys=on; insert into books(title,author_id) values('x',99);" 2>&1 | grep -q FOREIGN; then echo "FK error: OK"; fi
rm -rf "$T"

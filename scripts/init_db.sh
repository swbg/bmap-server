#!/bin/bash

DB_PATH="../data/main.db"
ENTRIES_CSV="../data/entries.csv"
PLACES_CSV="../data/places.csv"
PRODUCTS_CSV="../data/products.csv"

# 1. Delete old DB
rm -f "$DB_PATH"

# 2. Create schema from SQL (you must define tables in init_db.sql)
sqlite3 "$DB_PATH" < init_db.sql

# 3. Import CSVs in one sqlite3 session
sqlite3 "$DB_PATH" <<EOF
.separator ","

.import '$ENTRIES_CSV' entries
.import '$PLACES_CSV' places
.import '$PRODUCTS_CSV' products
EOF

columns_places=("valid_until")
columns_entries=("valid_from" "last_update" "valid_until" "volume")

sql_commands="BEGIN TRANSACTION;"

# Clean places date columns
for column in "${columns_places[@]}"; do
    echo "Cleaning places.$column"
    sql_commands+="UPDATE places SET $column = NULL WHERE $column = ''; "
    sql_commands+="UPDATE places SET $column = NULL WHERE $column = ' '; "
done

# Clean entries date columns
for column in "${columns_entries[@]}"; do
    echo "Cleaning entries.$column"
    sql_commands+="UPDATE entries SET $column = NULL WHERE $column = ''; "
    sql_commands+="UPDATE entries SET $column = NULL WHERE $column = ' '; "
done

sql_commands+="COMMIT;"

echo "$sql_commands" | sqlite3 "$DB_PATH"

echo "All operations completed. DB is set up"
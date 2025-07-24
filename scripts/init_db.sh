#!/bin/bash

rm ../data/main.db
sqlite3 ../data/main.db \
    ".read init_db.sql" \
    ".separator ," \
    ".mode csv entries" \
    ".mode csv places" \
    ".mode csv products" \
    ".import ../data/entries.csv entries" \
    ".import ../data/places.csv places" \
    ".import ../data/products.csv products"

CREATE TABLE IF NOT EXISTS entries (
  entry_id INTEGER PRIMARY KEY,
  place_id INTEGER,
  product_id INTEGER,
  price INTEGER,
  volume INTEGER,
  vom_fass BOOLEAN,

  valid_from TEXT NOT NULL,
  last_update TEXT NOT NULL,
  valid_until TEXT,

  FOREIGN KEY (place_id) REFERENCES places,
  FOREIGN KEY (product_id) REFERENCES products
);

CREATE TABLE IF NOT EXISTS places (
  place_id INTEGER PRIMARY KEY,

  lat REAL NOT NULL,
  lon REAL NOT NULL,

  place_name TEXT NOT NULL,
  place_type TEXT,
  address TEXT,

  website TEXT,
  phone TEXT,
  note TEXT,
  valid_until TEXT
);

CREATE TABLE IF NOT EXISTS products (
  product_id INTEGER PRIMARY KEY,
  brand_name TEXT,
  product_name TEXT NOT NULL,
  product_type TEXT NOT NULL
);

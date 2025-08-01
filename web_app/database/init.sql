CREATE TABLE IF NOT EXISTS tasks (
id INTEGER PRIMARY KEY AUTOINCREMENT
, done INTEGER NOT NULL CHECK(done IN (0, 1))
, title TEXT NOT NULL CHECK(length(title) > 0)
, due TEXT NOT NULL  -- Хранение даты в формате ISO8601 (YYYY-MM-DD)
, tech_date_add TEXT NOT NULL  -- ISO8601 для даты и времени
, tech_date_end TEXT NOT NULL
)
;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT
, email TEXT NOT NULL UNIQUE CHECK(email LIKE '%_@__%.__%')
, password TEXT NOT NULL CHECK(length(password) >= 8)
, tech_date_registration TEXT NOT NULL DEFAULT (datetime('now'))
)
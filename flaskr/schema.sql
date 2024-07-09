DROP TABLE IF EXISTS towers;

CREATE TABLE towers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    radius REAL NOT NULL,
    status TEXT NOT NULL
);
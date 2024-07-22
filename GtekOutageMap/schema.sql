DROP TABLE IF EXISTS towers;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS post_updates;

CREATE TABLE towers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    radius REAL NOT NULL,
    status TEXT NOT NULL
);

-- INSERT INTO towers (name, latitude, longitude, radius, status) VALUES ("Patrick Farms GE",27.6701583531,-97.9140368697,4,"active");
-- INSERT INTO towers (name, latitude, longitude, radius, status) VALUES ("Alice Fire Department",27.7533776428,-98.0707372187,10,"active");

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    status TEXT NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE post_updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    update_content TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id)
);
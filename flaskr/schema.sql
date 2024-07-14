DROP TABLE IF EXISTS towers;

CREATE TABLE towers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    radius REAL NOT NULL,
    status TEXT NOT NULL
);

INSERT INTO towers (name, latitude, longitude, radius, status) VALUES ("Patrick Farms GE",27.6701583531,-97.9140368697,4,"active");
INSERT INTO towers (name, latitude, longitude, radius, status) VALUES ("Alice Fire Department",27.7533776428,-98.0707372187,10,"active");
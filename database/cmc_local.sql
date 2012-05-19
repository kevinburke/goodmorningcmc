PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE cmc (
    the_name string not null,
    host string not null,
    port integer not null
);
INSERT INTO "cmc" VALUES('cmc','127.0.0.1',5000);
CREATE TABLE weather (
    id integer primary key autoincrement,
    image_url string not null,
    high string not null,
    low string not null,
    condition string not null
);
INSERT INTO "weather" VALUES(1,'http://google.com/ig',80,57,'sunny');
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('weather',1);
COMMIT;

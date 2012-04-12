drop table if exists weather;
drop table if exists sitename;
create table weather (
    id integer primary key autoincrement,
    image_url string not null,
    high string not null,
    low string not null,
    condition string not null
);
create table sitename (
    the_name string not null,
    host string not null,
    port integer not null
);

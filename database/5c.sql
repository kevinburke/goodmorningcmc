drop table if exists weather;
drop table if exists cmc;
drop table if exists pomona;
drop table if exists scripps;
create table weather (
    id integer primary key autoincrement,
    image_url string not null,
    high string not null,
    low string not null,
    condition string not null
);
create table cmc (
    the_name string not null,
    host string not null,
    port integer not null
);
create table pomona (
    the_name string not null,
    host string not null,
    port integer not null
);
create table scripps (
    the_name string not null,
    host string not null,
    port integer not null
);
insert into weather(image_url, high, low, condition) values("http://google.com/ig","80","57","sunny");
insert into cmc(the_name, host, port) values("cmc","0.0.0.0", 50094);
insert into scripps(the_name, host, port) values("scripps","0.0.0.0", 50094);
insert into pomona(the_name, host, port) values("pomona","0.0.0.0", 50094);

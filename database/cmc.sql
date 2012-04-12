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
create table phoneno (
    phoneno string not null
);
insert into weather(image_url, high, low, condition) values("http://google.com/ig","80","57","sunny");
insert into sitename(the_name, host, port) values("cmc","0.0.0.0", 28334);
insert into phoneno(phoneno) values ("9252717005");

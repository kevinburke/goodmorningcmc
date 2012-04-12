drop table if exists weather;
drop table if exists sitename;
drop table if exists phoneno;
drop table if exists site_config;
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
create table site_config (
    name string not null,
    base_url string not null,
    title string not null,
    tagline string not null,
    description string not null,
    calltoaction_title string not null,
    calltoaction_text string not null,
    fb_src string not null,
    facebooklink string not null,
    twitter string not null,
    contact string not null,
    font_name string not null,
    font_file_name string not null,
    font_woff_name string not null,
    font_ttf_name string not null,
    font_svg_name string not null,
    bigimage string not null,
    bigimagealt string not null,
    bigimagetitle string not null,
    button_url string not null,
    titlefont string not null,
    litecolor string not null,
    color string not null,
    hover_color string not null,
    formaction string not null,
    post_json string not null,
    og_type string not null,
    og_image string not null,
    og_site_name string not null,
    analytics string not null
);

insert into site_config (
    name,
    base_url,
    title,
    tagline,
    description,
    calltoaction_title,
    calltoaction_text,
    fb_src,
    facebooklink,
    twitter,
    contact,
    font_name,
    font_file_name,
    font_woff_name,
    font_ttf_name,
    font_svg_name,
    bigimage,
    bigimagealt,
    bigimagetitle,
    button_url,
    titlefont,
    litecolor,
    color,
    hover_color,
    formaction,
    post_json,
    og_type,
    og_image,
    og_site_name,
    analytics
) values (
    -- name
    "cmc",
    -- base_url
    "goodmorningcmc.com",
    -- title
    "Good Morning CMC",
    -- tagline
    "The Useful E-Newsletter for Claremont McKenna Students",
    -- description
    "Good Morning CMC is a daily email that helps you keep your finger on the campus pulse. Over 500 CMCers subscribe. Sign up today.",
    -- calltoaction_title
    "Over 500 CMCers start their day with Good Morning CMC.",
    -- calltoaction_text
    "Designed by a student to be useful for students. Get a daily email with campus events, sports updates, relevant campus and world news, the weather, and what's in the dining halls. You should subscribe today.",
    -- fb_src
    "http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Fgoodmorningcmc.com&amp;layout=standard&amp;show_faces=true&amp;width=450&amp;action=like&amp;font=arial&amp;colorscheme=light&amp;height=80",
    -- facebooklink
    "http://www.facebook.com/pages/Good-Morning-CMC/113073532088790",
    -- twitter
    "http://twitter.com/goodmorningcmc",
    -- contact
    "kevin@goodmorningcmc.com",
    -- font_name
    "MachineScriptRegular",
    -- font_file_name
    "MachineScriptRegular.eot",
    -- font_woff_name
    "MachineScriptRegular.woff",
    -- font_ttf_name
    "MachineScriptRegular.ttf",
    -- font_svg_name
    "MachineScriptRegular.svg#webfont9l6uWoHA",
    -- bigimage
    "plate.jpg",
    -- bigimagealt
    "Good Morning CMC spelled out with sausage and eggs",
    -- bigimagetitle
    "Photo credit: Caroline Nyce '13",
    -- button_url
    "cmc/button.png",
    -- titlefont
    "MachineScript",
    -- litecolor
    "#a31a2f",
    -- color
    "#740e1c",
    -- hover_color
    "#ffcc00",
    -- formaction
    "http://kburke.us1.list-manage.com/subscribe/post?u=2c913f03099b6ba1915c7f8d9&id=2f72f64ad3",
    -- post_json
    "http://kburke.us1.list-manage.com/subscribe/post-json?u=2c913f03099b6ba1915c7f8d9&id=2f72f64ad3&c=?",
    -- og_type
    "website",
    -- og_image
    "plate.jpg",
    -- og_site_name
    "Good Morning CMC",
    -- analytics
    "UA-566397-4"
);

insert into weather(image_url, high, low, condition) values("http://google.com/ig","80","57","sunny");
insert into sitename(the_name, host, port) values("cmc","127.0.0.1",5000);
insert into phoneno(phoneno) values ("9252717005");

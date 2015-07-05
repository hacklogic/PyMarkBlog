drop table if exists blog;
create table blog (
  id integer primary key autoincrement,
  title text not null,
  content text,
  post_time datetime
);

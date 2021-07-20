DROP TABLE IF EXISTS content;


CREATE TABLE content{
    id integer primary key AUTOINCREMENT,
    task text NOT NULL,
    created_on datetime,
    due datetime,
    status text,
    description text
};
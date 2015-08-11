-- Copyright (C) 2011 Jack Grigg
-- Table structure for table 'Django User'

CREATE TABLE IF NOT EXISTS /*_*/authdjango (
    mw_user_id integer unsigned NOT NULL PRIMARY KEY,
    d_user_id integer unsigned,
    FOREIGN KEY (mw_user_id) REFERENCES /*_*/user (user_id)
    ) /*$wgDBTableOptions*/;

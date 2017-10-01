# This can safely be removed some time after it has been run

# This script cleans up some old cruft in the database and
# migrates the content-app things.

DROP TABLE gallery_album;
DROP TABLE gallery_picture;
DROP TABLE quotes_quote;
DROP TABLE sessionprofile_sessionprofile;
DROP TABLE south_migrationhistory;
# DROP TABLE content_archiveentries;
# DROP TABLE content_archive;
DROP TABLE content_splashconfig;


DELETE FROM django_content_type WHERE app_label='events';
DELETE FROM django_content_type WHERE app_label='news';
DELETE FROM django_content_type WHERE app_label='gallery';
DELETE FROM django_content_type WHERE app_label='south';
DELETE FROM django_content_type WHERE app_label='quotes';

UPDATE django_content_type SET app_label='album' WHERE app_label='content' AND model='album';
UPDATE django_content_type SET app_label='album' WHERE app_label='content' AND model='albumimage';
UPDATE django_content_type SET app_label='blog' WHERE app_label='content' AND model='blog';
UPDATE django_content_type SET app_label='blog' WHERE app_label='content' AND model='blogpost';
UPDATE django_content_type SET app_label='image' WHERE app_label='content' AND model='contentimage';
UPDATE django_content_type SET app_label='events' WHERE app_label='content' AND model='event';
UPDATE django_content_type SET app_label='events' WHERE app_label='content' AND model='eventregistration';
UPDATE django_content_type SET app_label='news' WHERE app_label='content' AND model='news';

DELETE FROM django_content_type WHERE app_label='content';


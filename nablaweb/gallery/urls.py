from django.conf.urls.defaults import *


urlpatterns = patterns('gallery.views',
    (r'^$','index'),
    (r'^album/(?P<album_id>\d{1,8})/$', 'album'),
    (r'^album/(?P<album_id>\d{1,8})/picture/(?P<picture_number>\d{1,8})/$', 'picture_large'),
    (r'^album/(?P<album_id>\d{1,8})/add/$', 'new_image_form'),
    (r'^album/(?P<album_id>\d{1,8})/delete/(?P<picture_id>\d{1,8})/$', 'delete_picture'),
    (r'^album/add/$', 'new_album'),
    (r'^album/delete/(?P<album_id>\d{1,8})/conf/(?P<confirmation>\d{1})/$', 'delete_album'),
)

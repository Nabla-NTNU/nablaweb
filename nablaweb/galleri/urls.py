from django.conf.urls.defaults import *


urlpatterns = patterns('gallery.views',
    (r'^$','index'),
    (r'^album/(?P<album_id>\d+)/$', 'album'),
    (r'^album/(?P<album_id>\d+)/picture/(?P<picture_number>\d+)/$', 'picture_large'),
    (r'^album/(?P<album_id>\d+)/add/$', 'new_image_form'),
    (r'^album/(?P<album_id>\d+)/delete/(?P<picture_id>\d+)/$', 'delete_picture'),
    (r'^album/add/$', 'new_album'),
    (r'^album/delete/(?P<album_id>\d+)/conf/(?P<confirmation>\d{1})/$', 'delete_album'),
)

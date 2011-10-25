from django.conf.urls.defaults import *
from gallery.views import AlbumDeleteView

urlpatterns = patterns('gallery.views',
    (r'^$','index'),
    (r'^album/(?P<album_id>\d{1,8})/$', 'album'),
    (r'^album/(?P<album_id>\d{1,8})/edit/$', 'edit_album'),
    (r'^album/(?P<album_id>\d{1,8})/picture/(?P<album_picnr>\d{1,8})/$', 'picture_large'),
    (r'^album/(?P<album_id>\d{1,8})/add_pic/$', 'add_picture'),
    (r'^album/(?P<album_id>\d{1,8})/picture/(?P<picture_id>\d{1,8})/edit/$', 'edit_picture'),
    (r'^album/(?P<album_id>\d{1,8})/picture/(?P<picture_id>\d{1,8})/delete/$', 'delete_picture'),
    (r'^opprett/$', 'add_album'),
    
    (r'^album/(?P<pk>\d{1,8})/del/$', AlbumDeleteView.as_view()),
)

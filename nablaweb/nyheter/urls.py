from django.conf.urls.defaults import *

urlpatterns = patterns('nyheter.views',
    (r'^$', 'list_news'),
    (r'^vis/(?P<news_id>\d+)/$', 'show_news'),
    (r'^opprett/(?P<news_id>\d+)/$', 'create_news'),
    (r'^endre/(?P<news_id>\d+)/$', 'edit_news'),
    (r'^slett/(?P<news_id>\d+)/$', 'delete_news'),
)

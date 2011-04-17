from django.conf.urls.defaults import *

urlpatterns = patterns('nyheter.views',
    (r'^$', 'list_news'),
    (r'^(?P<news_id>\d+)/$', 'show_news'),
    (r'^opprett/$', 'create_news'),
    (r'^(?P<news_id>\d+)/endre/$', 'edit_news'),
    (r'^(?P<news_id>\d+)/slett/$', 'delete_news'),
)

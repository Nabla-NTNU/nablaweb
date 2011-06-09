from django.conf.urls.defaults import *

urlpatterns = patterns('nyheter.views',
    (r'^$', 'list_news'),
    (r'^(?P<news_id>\d{1,8})/$', 'show_news'),
    (r'^opprett/$', 'create_or_edit_news'),
    (r'^(?P<news_id>\d+)/endre/$', 'create_or_edit_news'),
    (r'^(?P<news_id>\d+)/slett/$', 'delete_news'),
)

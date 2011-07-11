from django.conf.urls.defaults import *


urlpatterns = patterns('news.views',
    (r'^$', 'list_news'),
    (r'^(?P<news_id>\d{1,8})/$', 'show_news'),
    (r'^opprett/$', 'create_or_edit_news'),
    (r'^(?P<news_id>\d{1,8})/endre/$', 'create_or_edit_news'),
    (r'^(?P<news_id>\d{1,8})/slett/$', 'delete_news'),
)

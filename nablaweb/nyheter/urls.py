from django.conf.urls.defaults import *

urlpatterns = patterns('nyheter.views',
    (r'^(?P<news_id>\d+)/$', 'show_news'),
)

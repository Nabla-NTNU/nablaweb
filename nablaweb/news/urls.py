# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from news.views import NewsDetailView, NewsListView
from news.feeds import RecentNews

urlpatterns = patterns('news.views',

    # Offentlig
    url(r'^$',
        NewsListView.as_view(),
        name='news_list'),
    url(r'^(?P<pk>\d{1,8})/(?P<slug>[-\w]*)$',
        NewsDetailView.as_view(),
        name='news_detail'),

)

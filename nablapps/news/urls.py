"""
Urls for news articles
"""
from django.conf.urls import url
from .views import NewsListView, NewsDetailView

urlpatterns = [
    url(r'^$',
        NewsListView.as_view(),
        name='news_list'),
    url(r'^(?P<pk>\d{1,8})/(?P<slug>[-\w]*)$',
        NewsDetailView.as_view(),
        name='news_detail'),
]

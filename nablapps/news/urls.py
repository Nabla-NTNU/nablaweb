"""
Urls for news articles
"""
from django.urls import path

from .views import NewsDetailView, NewsListView

urlpatterns = [
    path("", NewsListView.as_view(), name="news_list"),
    path(
        "<int:pk>/<str:slug>/",
        NewsDetailView.as_view(),
        name="news_detail",
    ),
]

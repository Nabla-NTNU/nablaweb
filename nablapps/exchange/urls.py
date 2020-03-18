from django.urls import path

from .views import (
    ExchangeFrontpageView,
    ExchangeListView,
    ExchangeNewsDetailView,
    ExchangeNewsView,
    InfoDetailView,
    UnivDetailView,
)

urlpatterns = [
    path("", ExchangeFrontpageView.as_view(), name="ex_frontpage"),
    path("info/(<int:pk>/", InfoDetailView.as_view(), name="info_detail"),
    path("<int:pk>/", UnivDetailView.as_view(), name="ex_detail_list"),
    path("exchange-list/", ExchangeListView.as_view(), name="ex_list"),
    path("exchange-news/", ExchangeNewsView.as_view(), name="ex_news"),
    path(
        "exchange-news/detail/<int:pk>/<str:slug>/",
        ExchangeNewsDetailView.as_view(),
        name="ex_news_detail",
    ),
]

from django.urls import path

from .views import PodcastDetailView, RssView, SeasonView

urlpatterns = [
    path("", SeasonView.as_view(), name="season_view"),
    path("season<int:number>/", SeasonView.as_view(), name="season_view"),
    path("<int:pk>/", PodcastDetailView.as_view(), name="podcast_detail"),
    path("subscribe.rss/", RssView.as_view(), name="season_rss"),
]

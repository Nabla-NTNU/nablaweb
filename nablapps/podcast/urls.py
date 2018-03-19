from django.conf.urls import url
from .views import SeasonView, PodcastDetailView, RssView

urlpatterns = [
    url(r'^$', SeasonView.as_view(), name='season_view'),
    url(r'^season(?P<number>\d+)$', SeasonView.as_view(), name='season_view'),
    url(r'^(?P<pk>\d+)/$', PodcastDetailView.as_view(), name='podcast_detail'),
    url(r'^subscribe.rss$', RssView.as_view(), name='season_rss_default'),
    url(r'^season(?P<number>\d+).rss$', RssView.as_view(), name='season_rss_select'),
]

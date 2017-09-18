# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import *
from .feeds.events import RecentEvents

urlpatterns = [
    url(r'^album/$',
        AlbumList.as_view(),
        name='albums'),
    url(r'^album/(?P<pk>\d{1,8})/(?P<num>\d{1,8})/$',
        AlbumImageView.as_view(),
        name='album_image'),
    url(r'^album/(?P<pk>\d{1,8})/$',
        AlbumOverview.as_view(),
        name='album'),

    url(r'^nyheter/$',
        NewsListView.as_view(),
        name='news_list'),
    url(r'^nyheter/(?P<pk>\d{1,8})/(?P<slug>[-\w]*)$',
        NewsDetailView.as_view(),
        name='news_detail'),

    url(r'^arrangement/(?P<pk>\d{1,8})/admin2$',
        AdministerRegistrationsView.as_view(),
        name='event_admin'),

    url(r'^arrangement/$',
        calendar,
        name='event_list'),

    url(r'^arrangement/(\d{4})/(\d{1,2})/$',
        calendar,
        name='event_list'),

    url(r'^mine/$',
        UserEventView.as_view(),
        name="view_user_events"),

    url(r'^arrangement/(?P<pk>\d{1,8})/registration$',
        RegisterUserView.as_view(),
        name='registration'),

    url(r'^arrangement/(?P<pk>\d{1,8})-(?P<slug>[-\w]*)$',
        EventDetailView.as_view(),
        name='event_detail'),

    url(r'^arrangement/reg/(?P<pk>\d{1,8})$',
        EventRegistrationsView.as_view(),
        name='event_registrations'),

    url(r'^arrangement/(?P<event_id>\d{1,8}).ics$',
        ical_event,
        name="ical_event"),

    url(r'^feed/$',
        RecentEvents(),
        name="event_feed"),

    url(r'^blogg/$',
        BlogListView.as_view(),
        name="blog"),

    url(r'^blogg/(?P<blog>[\w-]+)/$',
        BlogView.as_view(),
        name="blog"),

    url(r'^blogg/(?P<blog>[\w-]+)/(?P<slug>[\w-]+)$',
        BlogPostView.as_view(),
        name="blog_post"),
]

from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name="forum-index"),
    path('browse_channels/', BrowseChannelsView.as_view(), name="browse-channels"),
    path('<channel_id>/', ChannelIndexView.as_view(), name="channel-index"),

    path('test/<channel_id>/<thread_id>/', MainView.as_view(), name="main-view"),
]

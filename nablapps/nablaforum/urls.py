from django.urls import path

from .views import *

urlpatterns = [
   # path('', IndexView.as_view(), name="forum-index"),
    path('create_new_channel/', CreateChannelView.as_view(), name="create-channel"),
    path('browse_channels/', BrowseChannelsView.as_view(), name="browse-channels"),
   # path('<channel_id>/', ChannelIndexView.as_view(), name="channel-index"),
   # path('<channel_id>/<thread_id>/', ThreadView.as_view(), name="thread-view"),

    path('<channel_id>/<thread_id>/', MainView.as_view(), name="forum-main"),
]

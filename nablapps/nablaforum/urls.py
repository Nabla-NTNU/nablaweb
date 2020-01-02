from django.urls import path

from .views import *

urlpatterns = [
    path('<channel_id>/<thread_id>/', MainView.as_view(), name="forum-main"),
    path('create_new_channel/', CreateChannelView.as_view(), name="create-channel"),
    path('browse_channels/', BrowseChannelsView.as_view(), name="browse-channels"),
]

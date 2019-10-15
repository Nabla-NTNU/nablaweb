from django.urls import path

from .views import *

urlpatterns = [
    path('index/', IndexView.as_view(), name="forum-index"), # maybe index-view rather idk
    path('<channel_id>/', ChannelIndexView.as_view(), name="channel-index"),
    path('<channel_id>/<thread_id>/', ThreadView.as_view(), name="thread-view"),
]

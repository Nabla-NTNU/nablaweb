from django.urls import path

from .views import (
    CreateMailFeedView,
    MailFeedDetailView,
    MailFeedListView,
    SubscribeView,
)

urlpatterns = [
    path("", MailFeedListView.as_view(), name="mailfeed-list"),
    path(
        "detail/<int:mailfeed_id>/",
        MailFeedDetailView.as_view(),
        name="mailfeed-detail",
    ),
    path(
        "create-mailfeed/", CreateMailFeedView.as_view(), name="create-mailfeed"
    ),
    path(
        "subscribe/<int:mailfeed_id>/",
        SubscribeView.as_view(),
        name="subscribe-mailfeed",
    ),
]

from django.urls import path

from .views import (
    CreateEventView,
    EventDetailView,
    QrEventListView,
    RegisterTicketsView,
    ScanTicketView,
    UpdateTicketsView,
    render_ticket,
)

urlpatterns = [
    path("", QrEventListView.as_view(), name="qr-event-list"),
    path("detail/<int:pk>/", EventDetailView.as_view(), name="qr-event-detail"),
    path("create-qrevent/", CreateEventView.as_view(), name="create-qr-event"),
    path(
        "register/<int:qr_event_id>/<str:qr_ticket_id>/",
        RegisterTicketsView.as_view(),
        name="register_tickets",
    ),
    path(
        "render/<int:qr_event_id>/<str:qr_ticket_id>/",
        render_ticket,
        name="render",
    ),
    path("scan/", ScanTicketView.as_view(), name="scan"),
    path("scan/<str:ticket_id>", UpdateTicketsView.as_view(), name="register"),
]

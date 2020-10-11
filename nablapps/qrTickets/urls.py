from django.urls import path

from .views import EventDetailView, RegisterTicketsView, render_ticket, UpdateTicketsView, TicketList, TicketDetail, CreateEventView, QrEventListView

urlpatterns = [
    path("event-list/", QrEventListView.as_view(), name="qr-event-list"),
    path("detail/<int:pk>", EventDetailView.as_view(), name="qr-event-detail"),
    path("create-qrevent/", CreateEventView.as_view(), name="create_qr_event"),
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
    path("scan/<str:ticket_id>", UpdateTicketsView.as_view(), name="scan"),
    path("ticket-list/", TicketList.as_view(), name="ticket-list"),
    path("ticket-detail/<str:ticket_id>", TicketDetail.as_view(), name="ticket-detail"),
]

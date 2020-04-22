from django.urls import path

from .views import GenerateTicketsView, RegisterTicketsView, render_ticket, test

urlpatterns = [
    path("generate/", GenerateTicketsView.as_view(), name="generate_tickets"),
    path(
        "register/<int:qr_event_id>/<str:qr_ticket_id>/",
        RegisterTicketsView.as_view(),
        name="register_tickets",
    ),
    path("render/<int:qr_event_id>/<str:qr_ticket_id>/", render_ticket, name="render",),
    path("test/", test, name="test"),
]

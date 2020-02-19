from django.conf.urls import url

from .views import GenerateTicketsView, RegisterTicketsView, render_ticket, test

urlpatterns = [
    url(r"generate/$", GenerateTicketsView.as_view(), name="generate_tickets"),
    url(
        r"register/(?P<qr_event_id>[0-9]+)/(?P<qr_ticket_id>[\w\-]+)/$",
        RegisterTicketsView.as_view(),
        name="register_tickets",
    ),
    url(
        r"render/(?P<qr_event_id>[0-9]+)/(?P<qr_ticket_id>[\w\-]+)/$",
        render_ticket,
        name="render",
    ),
    url(r"test/$", test, name="test"),
]

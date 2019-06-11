from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'generate/$', generate_tickets, name='generate_tickets'),
    url(r'register/(?P<qr_event_id>[0-9]+)/$(?P<qr_ticket_id>[0-9]+)', register_tickets, name='register_tickets'),
    url(r'test/$', test, name='test'),
]



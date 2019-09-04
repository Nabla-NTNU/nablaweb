from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.contact, name='contact'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^gullkorn/$', views.feedback, {'template':'gullkorn.html', 'send_to':'redaktor@nabla.ntnu.no'}, name='gullkorn'),
    url(r'^success/$', views.success, name='success'),
]

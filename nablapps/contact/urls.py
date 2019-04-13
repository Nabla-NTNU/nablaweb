from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.contact, name='contact'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^feedback/success/$', views.success, name='success'),
]

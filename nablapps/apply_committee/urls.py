from django.urls import path
from . import views

urlpatterns = [path("", views.ApplicationView.as_view())]

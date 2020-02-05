from django.urls import path
from . import views

# This file is included from main url.py under url '^application/'
urlpatterns =[
    path("", views.ApplicationView.as_view(), name="apply-committee"),
    path("list/", views.ApplicationListView.as_view(), name="list-applicants")
]

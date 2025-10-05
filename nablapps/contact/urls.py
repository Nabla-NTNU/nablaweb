from django.urls import path

from . import views

urlpatterns = [
    path("", views.contact, name="contact"),
    path("feedback/", views.feedback, name="feedback"),
    path(
        "gullkorn/",
        views.feedback,
        {"template": "gullkorn.html", "send_to": "redaktor@nabla.no"},
        name="gullkorn",
    ),
    path("success/", views.success, name="success"),
    path("success_gullkorn/", views.success_gullkorn, name="success_gullkorn"),
    path("rombooking/", views.roombooking, name="rombooking"),
    path("utstyrbooking/", views.utstyrbooking, name="utstyrbooking"),
    path("for_bedrifter/", views.for_bedrifter, name="for_bedrifter"),
]

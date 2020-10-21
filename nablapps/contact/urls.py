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
]

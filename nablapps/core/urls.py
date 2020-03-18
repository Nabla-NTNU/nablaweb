from django.urls import path

from .views import AboutView

urlpatterns = [
    path("", AboutView.as_view(), name="om-nabla"),
]

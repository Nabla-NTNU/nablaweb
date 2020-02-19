from django.conf.urls import url

from .views import AboutView

urlpatterns = [
    url(r"^$", AboutView.as_view(), name="om-nabla"),
]

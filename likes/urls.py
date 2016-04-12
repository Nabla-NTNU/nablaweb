from django.conf.urls import url
from .views import toggle_like_view


urlpatterns = [
    url(r'^toggle/$', toggle_like_view, name="toggle_like"),
]

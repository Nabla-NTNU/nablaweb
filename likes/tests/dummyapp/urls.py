from django.conf.urls import url
from .views import DummyList


urlpatterns = [
    url(r'^list/$', DummyList.as_view(), name="dummy_list"),
]

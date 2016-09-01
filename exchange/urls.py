from django.conf.urls import url
from .views import ExDetailListView, ExchangeListView


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', ExDetailListView.as_view(), name="ex_detail_list"),
    url(r'^$', ExchangeListView.as_view(), name="ex_list"),
]
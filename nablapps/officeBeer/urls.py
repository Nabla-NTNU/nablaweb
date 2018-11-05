"""
Urls for office beer
"""

from django.conf.urls import url
from .views import AccountView, PurchaseView

urlpatterns = [
    url(r'^$',
        AccountView.as_view(),
        name='officebeer_account'),
    url(r'^purchase$',
        PurchaseView.as_view(),
        name="officebeer_purchase"),
]

"""
Urls for office beer
"""

from django.urls import path

from .views import AccountView, DepositRequestView, PurchaseView

urlpatterns = [
    path("", AccountView.as_view(), name="officebeer_account"),
    path("purchase/", PurchaseView.as_view(), name="officebeer_purchase"),
    path("deposit/", DepositRequestView.as_view(), name="officebeer_deposit"),
]

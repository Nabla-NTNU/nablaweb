from django.urls import path

from .views import (
    CategoryDetailView,
    IndexView,
    OrderSummaryView,
    ProductDetailView,
    add_to_cart,
    remove_from_cart,
    remove_single_product_from_cart,
)

app_name = "nablashop"
urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path(
        "product/<int:pk>/",
        view=ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "category/<int:pk>/",
        view=CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path("add-to-cart/<slug>/", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug>/", remove_from_cart, name="remove-from-cart"),
    path("order-summary/", OrderSummaryView.as_view(), name="order-summary"),
    path(
        "remove-product-from-cart/<slug>/",
        remove_single_product_from_cart,
        name="remove-single-product-from-cart",
    ),
]

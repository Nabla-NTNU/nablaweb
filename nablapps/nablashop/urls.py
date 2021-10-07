from django.urls import path

from .views import CategoryDetailView, IndexView, ProductDetailView

app_name = "nablashop"
urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("product/<int:pk>/", view=ProductDetailView.as_view(), name="product_detail",),
    path(
        "category/<int:pk>/", view=CategoryDetailView.as_view(), name="category_detail",
    ),
]

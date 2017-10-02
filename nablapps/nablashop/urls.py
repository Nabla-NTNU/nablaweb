from django.conf.urls import url
from .views import IndexView, ProductDetailView, CategoryDetailView


app_name = "nablashop"
urlpatterns = [
    url(r'^$', view=IndexView.as_view(), name='index'),
    url(r'^product/(?P<pk>[0-9]+)/$', view=ProductDetailView.as_view(), name='product_detail'),
    url(r'^category/(?P<pk>[0-9]+)/$', view=CategoryDetailView.as_view(), name='category_detail')
]

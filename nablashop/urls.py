from django.conf.urls import url
from . import views

app_name = "nablashop"
urlpatterns = [
    url(r'^$', view=views.index, name='index'),
    url(r'^product/(?P<product_id>[0-9]+)/$', view=views.product_detail, name='product_detail'),
    url(r'^category/(?P<category_id>[0-9]+)/$', view=views.category_detail, name='category_detail')
]
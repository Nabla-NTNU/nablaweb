from django.conf.urls import url

from skraattcast import views

urlpatterns = [
        url(r'^$', views.index, name='skraattcast_index')
]


from django.conf.urls import url

from skraattcast import views

urlpatterns = [
        url(r'^$', views.index, name='skraattcast_index'),
        url(r'^(?P<skraattcast_id>\d{1,8})$', views.play, name='skraattcast_play')
]


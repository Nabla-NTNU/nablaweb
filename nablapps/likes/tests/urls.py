from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^likes/', include('nablapps.likes.urls')),
    url(r'^dummy/', include('nablapps.likes.tests.dummyapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

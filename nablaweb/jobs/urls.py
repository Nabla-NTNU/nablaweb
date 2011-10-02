# -*- coding: utf-8 -*-

# URL-er for stillingsannonser-appen

from django.conf.urls.defaults import *
from nablaweb.jobs.views import *

urlpatterns = patterns('',
    (r'^stillinger/', List.as_view('ACME')),
    (r'^stillinger/(?P<year>\d{4})/$', 'jobs.views.datelist'),
    (r'^stillinger/(?P<year>\d{4})/(?P<month>\d{2})/$', 'jobs.views.datelist'),
    (r'^stillinger/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'jobs.views.datelist'),
    (r'^stillinger/(?P<company>\D{}/$)', 'jobs.views.companylist'),
    (r'^stillinger/(?P<company>\D{}/(?P<jobid>\d{3}/$', 'jobs.views.jobview')
)

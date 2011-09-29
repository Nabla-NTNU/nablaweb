# -*- coding: utf-8 -*-

# URL-er for stillingsannonser-appen

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^jobs/(?P<year>\d{4})/$', 'jobs.views.datelist'),
    (r'^jobs/(?P<year>\d{4})/(?P<month>\d{2})/$', 'jobs.views.datelist'),
    (r'^jobs/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'jobs.views.datelist'),
    (r'^jobs/(?P<company>\D{}/$)', 'jobs.views.companylist'),
    (r'^jobs/(?P<company>\D{}/(?P<jobid>\d{3}/$', 'jobs.views.jobview')
)

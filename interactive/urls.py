from django.conf.urls import patterns, url
from .views import AdventCalendarView, AdventDoorView

urlpatterns = \
    patterns('',
             url(r'^julekalender/(?P<year>\d+)/(?P<number>\d+)/$',
                 AdventDoorView.as_view(),
                 name="advent_door"),
             url(r'^julekalender/(?P<year>\d+)/$',
                 AdventCalendarView.as_view(),
                 name="advent_calendar"),

             )


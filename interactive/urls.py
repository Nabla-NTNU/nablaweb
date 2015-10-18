from django.conf.urls import url
from .views import AdventCalendarView, AdventDoorView

urlpatterns = [
     url(r'^julekalender/(?P<year>\d+)/(?P<number>\d+)/$',
         AdventDoorView.as_view(),
         name="advent_door"),
     url(r'^julekalender/(?P<year>\d+)/$',
         AdventCalendarView.as_view(),
         name="advent_calendar"),
]

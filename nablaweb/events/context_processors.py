# -*- coding: utf-8 -*-

from events.models import Event
from datetime import date
import calendar
def upcoming_events(request):
    """Legger globalt til en template-variabel upcoming_events"""

    # TODO: Denne må filtreres slik at den ikke viser eldre events
    upcoming_events = Event.objects.all()[:6]

    return {'upcoming_events': upcoming_events}

class Day(object):
    def __init__(self, arr, day):
        self.arr = arr
        self.date =day 
    
    def __unicode__(self):
        return u'<Dayobject: dag:%s arr:%s' % (self.date,self.arr)
    def __str__(self):
        return __unicode__(self)


def current_month_calendar(request):
    today = date.today()
    month = today.month
    year = today.year
    first_day_current_month = date(year,month,1)
    first_day_next_month = date(year,month+1,1) if month!=12 else date(year+1,1,1)
    numdays = calendar.mdays[month]
    events_of_month = Event.objects.filter(event_start__gt=first_day_current_month, event_start__lt=first_day_next_month)

    days =[Day(True,i+1) if bool(events_of_month.filter(event_start=date(year,month,i+1)))  else Day(False,i+1) for i in range(numdays) ]

    return {'dager': days, 'currentDate': today}

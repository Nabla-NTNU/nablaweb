# -*- coding: utf-8 -*-

from events.models import Event
from bedpres.models import BedPres
from datetime import date, datetime
from itertools import chain
import calendar

def upcoming_events(request):
    """Legger globalt til en template-variabel upcoming_events, og upcoming_bedpresses"""
    now = datetime.now()
    upcoming_events = Event.objects.filter(event_start__gte=now).order_by('event_start')[:6]
    upcoming_bedpresses = BedPres.objects.filter(event_start__gte=now).order_by('event_start')[:6]
    upcoming = sorted(chain(upcoming_events,upcoming_bedpresses),cmp=lambda e1,e2: 1 if e1.event_start>e2.event_start else  -1)[:6]
    return {'upcoming_events': upcoming, 'upcoming_bedpresses': upcoming_bedpresses}

class Day(object):
    def __init__(self, arr, day):
        self.arr = arr
        self.date =day 
    
    def __unicode__(self):
        return u'<Dayobject: dag:%s arr:%s' % (self.date,self.arr)
    def __str__(self):
        return __unicode__(self)


# TODO: Blir denne brukt noe sted?
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

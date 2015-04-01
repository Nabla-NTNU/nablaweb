from django import template
from django.contrib.sites.models import Site
from django.utils.http import urlquote_plus

from pytz import timezone

register = template.Library()


@register.filter
def google_calendarize(event):
    """Return a URL for adding an event to Google Calendar"""

    # We use naive dates without timezone information. That means they are
    # stored in local Norway time. Google Calendar expects UTC time. To convert
    # our datetimes to UTC, we
    #   1. Make them timezone-aware by giving them the Europe/Oslo timezone.
    #   2. We can now convert the datetime to UTC using astimezone()
    tz = timezone("Europe/Oslo")
    utc = timezone("UTC")
    tfmt = '%Y%m%dT%H%M%SZ'

    convert_time = lambda dt: tz.localize(st).astimezone(utc).strftime(tfmt)
    st = event.event_start
    en = event.event_end and event.event_end or event.event_start

    dates = '%s%s%s' % (convert_time(st), '%2F', convert_time(en))
    name = urlquote_plus(event.headline)

    s = ['http://www.google.com/calendar/event?action=TEMPLATE',
         'text=' + name,
         'dates=' + dates,
         'sprop=website:' + urlquote_plus(Site.objects.get_current().domain),
         ]

    if event.location:
        s.append('location=' + urlquote_plus(event.location))
    s.append('trp=false')

    return "&".join(s)

google_calendarize.safe = True

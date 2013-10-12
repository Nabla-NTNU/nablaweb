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
    UTC = timezone("UTC")

    st = event.event_start
    st = tz.localize(st).astimezone(UTC)

    en = event.event_end and event.event_end or event.event_start
    en = tz.localize(en).astimezone(UTC)

    tfmt = '%Y%m%dT%H%M%SZ'
    dates = '%s%s%s' % (st.strftime(tfmt), '%2F', en.strftime(tfmt))
    name = urlquote_plus(event.headline)

    s = ('http://www.google.com/calendar/event?action=TEMPLATE&' +
     'text=' + name + '&' +
     'dates=' + dates + '&' +
     'sprop=website:' + urlquote_plus(Site.objects.get_current().domain))

    if event.location:
        s = s + '&location=' + urlquote_plus(event.location)

    return s + '&trp=false'

google_calendarize.safe = True

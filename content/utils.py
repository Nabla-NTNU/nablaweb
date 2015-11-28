from collections import defaultdict
from datetime import datetime, timedelta
from django.conf import settings


def group_events_by_day(events):
    """Groups a list of events by day.

    Events spanning multiple days are grouped multiple times.
    """
    day_dict = defaultdict(list)
    for e in events:
        for day in day_range(e.event_start, e.event_end):
            day_dict[day].append(e)
    return day_dict


def day_range(start, end):
    """Returns a list of days (ints) between start and end (datetime)."""
    end = start if (end is None or end < start) else end
    return range(start.day, end.day+1)


def set_cookie(response, key, value, days_expire = 7):
  if days_expire is None:
    max_age = 365 * 24 * 60 * 60
  else:
    max_age = days_expire * 24 * 60 * 60
  expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

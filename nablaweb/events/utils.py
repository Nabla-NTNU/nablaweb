from collections import defaultdict


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
    end = start if (end is None or end<start) else end
    return range(start.day, end.day+1)

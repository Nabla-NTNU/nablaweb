"""
Module for creation of a calendar of events.
"""
from calendar import HTMLCalendar
from collections import defaultdict
from datetime import date, timedelta

from django.utils.html import conditional_escape as esc


class EventCalendar(HTMLCalendar):
    """
    Class for rendering models in a calendar, based on HTMLCalendar_.

    .. _HTMLCalendar: http://hg.python.org/cpython/file/2.7/Lib/calendar.py
    """
    day_full = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag',
                'Fredag', 'Lørdag', 'Søndag']

    def __init__(self, events, year, month):
        super().__init__()
        self.year, self.month = year, month
        self.events_grouped_by_day = group_events_by_day(events, month)

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        self.year, self.month = theyear, themonth

        start_tag = '<div class="month">'
        week_header = self.formatweekheader()
        weeks = [self.formatweek(week)
                 for week in self.monthdays2calendar(theyear, themonth)]
        week_string = "\n".join(weeks)
        end_tag = '</div>'
        return '\n'.join([start_tag, week_header, week_string, end_tag])

    def formatweekheader(self):
        """
        Return a header for a week as a table row.
        """
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        return f'<ul class="daynames">{s}</ul>'

    def formatweekday(self, day):
        """Return html list element for the given day"""
        return f'<li class="dayname">{self.day_full[day]}</li>'

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return f'<ul class="week">{s}</ul>'

    def formatday(self, day, weekday):
        """Returns the body of a single day formatted as a list"""
        html_event_list = self.format_event_list(day)
        css_classes = self.get_css_day_classes(day, weekday)
        if html_event_list:
            css_classes.append("filled")

        day_string = f'''
            <div class="date">
                <span class="day">{self.day_full[weekday]}</span>
                <span class="num">{day}.</span>
            </div>{html_event_list}\n'''
        joined_css_classes = " ".join(css_classes)
        return f'<li class="cell {joined_css_classes}">{day_string}</li>'

    def get_css_day_classes(self, day, weekday):
        """Get css class for the given day"""
        css_classes = self.cssclasses[weekday].split(" ")
        if day == 0:
            css_classes.append("noday")
        elif date.today() == date(self.year, self.month, day):
            css_classes.append('today')
        return css_classes

    def format_event_list(self, day):
        """Return html list of events on the given day"""
        events_list = self.events_grouped_by_day.get(day, [])
        list_items = list(map(self.format_event_list_item, events_list))
        return "".join(['<ul>'] + list_items + ['</ul>']) if list_items else ""

    @staticmethod
    def format_event_list_item(event):
        """Return html list element for the given event"""
        url = event.get_absolute_url()
        name = esc(event.get_short_name())
        return f'<li><a href="{url}">{name}</a></li>\n'


def group_events_by_day(events, month):
    """Groups a list of models by day.

    Events spanning multiple days are grouped multiple times.
    """
    day_dict = defaultdict(list)
    for e in events:
        end = e.event_start if (e.event_end is None or e.event_end < e.event_start) else e.event_end
        for day in day_range(e.event_start, end + timedelta(1)):
            if day.month == month:
                day_dict[day.day].append(e)
    return day_dict


def day_range(start, end):
    """Return iterator of datetimes for each day between start and end"""
    end = start if (end is None or end < start) else end
    for n in range(int((end - start).days)):
        yield start + timedelta(days=n)

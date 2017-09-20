from calendar import HTMLCalendar
from collections import defaultdict
from datetime import date

from django.utils.html import conditional_escape as esc


class EventCalendar(HTMLCalendar):
    """
    Class for rendering models in a calendar, based on HTMLCalendar_.

    .. _HTMLCalendar: http://hg.python.org/cpython/file/2.7/Lib/calendar.py
    """
    day_full = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag',
                'Fredag', 'Lørdag', 'Søndag']

    def __init__(self, events):
        super().__init__()
        self.events_grouped_by_day = group_events_by_day(events)

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
        return '<ul class="daynames">{}</ul>'.format(s)

    def formatweekday(self, i):
        return '<li class="dayname">{}</li>'.format(self.day_full[i])

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return '<ul class="week">{}</ul>'.format(s)

    def formatday(self, day, weekday):
        """Returns the body of a single day formatted as a list"""

        html_event_list = self.format_event_list(day)
        css_classes = self.get_css_day_classes(day, weekday)
        if html_event_list:
            css_classes.append("filled")

        day_format_string = '''
            <div class="date">
                <span class="day">{weekday}</span>
                <span class="num">{day}.</span>
            </div>{body}\n'''
        day_string = day_format_string.format(
            weekday=self.day_full[weekday],
            day=day,
            body=html_event_list
        )
        return '<li class="cell {css_classes}">{day_string}</li>'.format(
            css_classes=" ".join(css_classes),
            day_string=day_string)

    def get_css_day_classes(self, day, weekday):
        css_classes = self.cssclasses[weekday].split(" ")
        if day == 0:
            css_classes.append("noday")
        elif date.today() == date(self.year, self.month, day):
            css_classes.append('today')
        return css_classes

    def format_event_list(self, day):
        events_list = self.events_grouped_by_day.get(day, [])
        list_items = list(map(self.format_event_list_item, events_list))
        if list_items:
            return "".join(['<ul>'] + list_items + ['</ul>'])
        else:
            return ""

    @staticmethod
    def format_event_list_item(event):
        return '<li><a href="{url}">{name}</a></li>\n'.format(
            url=event.get_absolute_url(),
            name=esc(event.get_short_name())
        )


def group_events_by_day(events):
    """Groups a list of models by day.

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

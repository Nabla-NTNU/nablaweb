# -*- coding: utf-8 -*-
from calendar import HTMLCalendar
from datetime import date

from django.utils.html import conditional_escape as esc

day_full = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', u'Lørdag', u'Søndag']
day_abbr = ['Man', 'Tir', 'Ons', 'Tor', 'Fre', u'Lør', u'Søn']


def day_range(start, end):
    if not end:
        return [start.day] 
    num_days = (end-start).days + 1 
    return [start.day+i for i in range(num_days)]


class EventCalendar(HTMLCalendar):
    """
    Class for rendering events in a calendar, based on HTMLCalendar_.

    .. _HTMLCalendar: http://hg.python.org/cpython/file/2.7/Lib/calendar.py
    """

    def __init__(self, events):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):
        """Returns the body of a single day formatted as a list"""

        body_str = self.format_event_list(day)
        css_classes = self.get_css_day_classes(day, weekday)
        if body_str:
            css_classes.append("filled")

        day_format_string = u'''
            <div class="date">
                <span class="day">{weekday}</span>
                <span class="num">{day}.</span>
            </div>{body}\n'''
        day_string = day_format_string.format(
            weekday=day_full[weekday],
            day=day,
            body=body_str
        )
        return self.day_cell(" ".join(css_classes), day_string)

    def get_css_day_classes(self, day, weekday):
        css_classes = self.cssclasses[weekday].split(" ")
        if day == 0:
            css_classes.append("noday")
        elif date.today() == date(self.year, self.month, day):
            css_classes.append('today')
        return css_classes

    def format_event_list(self, day):
        events_list = self.events.get(day, [])
        list_items = [self.format_event_list_item(event)
                      for event in events_list]
        if list_items:
            return u"".join([u'<ul>'] + list_items + [u'</ul>'])
        else:
            return u""

    def format_event_list_item(self, event):
        return u'<li><a href="{url}">{name}</a></li>\n'.format(
            url=event.get_absolute_url(),
            name=esc(event.get_short_name())
        )

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return '<ul class="week">%s</ul>' % s

    def formatweekday(self, i):
        return '<li class="dayname">%s</li>' % day_full[i];

    def formatweekheader(self):
         """
         Return a header for a week as a table row.
         """
         s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
         return '<ul class="daynames">%s</ul>' % s

    def group_by_day(self, events):
        day_dict = {}
        for e in events:
            for day in day_range(e.event_start, e.event_end):
                day_dict.setdefault(day, []).append(e)
        return day_dict

    def day_cell(self, cssclass, body):
        return '<li class="cell %s">%s</li>' % (cssclass, body)

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
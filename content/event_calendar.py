# -*- coding: utf-8 -*-
from calendar import HTMLCalendar
from datetime import date

from django.utils.html import conditional_escape as esc

from content.utils import group_events_by_day


class EventCalendar(HTMLCalendar):
    """
    Class for rendering events in a calendar, based on HTMLCalendar_.

    .. _HTMLCalendar: http://hg.python.org/cpython/file/2.7/Lib/calendar.py
    """
    day_full = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag',
                'Fredag', u'Lørdag', u'Søndag']

    def __init__(self, events):
        super(EventCalendar, self).__init__()
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
        return u'<ul class="daynames">{}</ul>'.format(s)

    def formatweekday(self, i):
        return u'<li class="dayname">{}</li>'.format(self.day_full[i])

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return u'<ul class="week">{}</ul>'.format(s)

    def formatday(self, day, weekday):
        """Returns the body of a single day formatted as a list"""

        html_event_list = self.format_event_list(day)
        css_classes = self.get_css_day_classes(day, weekday)
        if html_event_list:
            css_classes.append("filled")

        day_format_string = u'''
            <div class="date">
                <span class="day">{weekday}</span>
                <span class="num">{day}.</span>
            </div>{body}\n'''
        day_string = day_format_string.format(
            weekday=self.day_full[weekday],
            day=day,
            body=html_event_list
        )
        return u'<li class="cell {css_classes}">{day_string}</li>'.format(
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
            return u"".join([u'<ul>'] + list_items + [u'</ul>'])
        else:
            return u""

    @staticmethod
    def format_event_list_item(event):
        return u'<li><a href="{url}">{name}</a></li>\n'.format(
            url=event.get_absolute_url(),
            name=esc(event.get_short_name())
        )

# -*- coding: utf-8 -*-
from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

day_full = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', u'Lørdag', u'Søndag']
day_abbr = ['Man', 'Tir', 'Ons', 'Tor', 'Fre', u'Lør', u'Søn']

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
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                body = ['<ul>']
                for event in self.events[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % event.get_absolute_url())
                    # TODO: Use event.headline if short_name does not exist
                    body.append(esc(event.get_short_name()))
                    body.append('</a></li>')
                body.append('</ul>')

                return self.day_cell(cssclass, 
                    '<div class="date"><span class="day">%s </span><span class="num">%d.</span></div> %s' % 
                    (day_full[weekday], day, ''.join(body)))

            return self.day_cell(cssclass, 
                '<div class="date"><span class="day">%s </span><span class="num">%d.</span></div>' % 
                (day_full[weekday], day))

        return self.day_cell('noday', '&nbsp;')

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return '<ul class="week">%s</ul>' % s

    def formatmonth(self, year, month):
        """Returns a whole month"""
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def formatweekday(self, i):
        return '<li class="dayname">%s</li>' % day_full[i];

    def formatweekheader(self):
         """
         Return a header for a week as a table row.
         """
         s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
         return '<ul class="daynames">%s</ul>' % s


    def group_by_day(self, events):
        field = lambda event: event.event_start.day
        return dict(
                [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<li class="cell %s">%s</li>' % (cssclass, body)


    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        self.year, self.month = theyear, themonth
        v = []
        a = v.append
        a('\n')
        a('<div class="month">')
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</div>')
        a('\n')
        return ''.join(v)



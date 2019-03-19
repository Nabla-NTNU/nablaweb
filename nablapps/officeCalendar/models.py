from django.db import models
from django.conf import settings # AUTH_USER_MODEL
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta
from collections import defaultdict

class OfficeEvent(models.Model):
    """Event in the office. Used as an internal calendar for office use."""

    start_time = models.DateTimeField(blank = False)
    duration   = models.DurationField(blank = False, help_text="HH:MM", default="01:00")
    contact_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    title = models.CharField(max_length = 30)
    description = models.TextField(blank = True)

    @property
    def end_time(self):
        return self.start_time + self.duration

    def duration_natural(self):
        """Return a natural language string with length of duration"""

        hours, minutes = self.duration.seconds/3600, (self.duration.seconds//60)%60

        if hours < 1:
            return f"{minutes} minutter"

        plural_suffix = '' if hours == 1 else 'r'
        return f"{hours:.1g} time{plural_suffix}"

    def clean(self):
        # We only support events spanning one day
        if (self.start_time.date() != self.end_time.date()):
            raise ValidationError("start_time and end_time must be on the same day!")

    def get_office_event_week():
        """Returns a dict with this weeks officeEvents in a dictionary with weekday as key and list of events for that day as value
        Requires datetime and defaultdict to be imported"""

        now = datetime.now()

        end_of_week = now + timedelta(days = ( 6 - now.weekday() ))
        end_of_week = end_of_week.date()

        # Find events this week, but ignore those that have happened
        office_events = OfficeEvent.objects.filter(start_time__date__gte = now, start_time__date__lte = end_of_week).order_by('start_time')
        day_dict = defaultdict(list)

        for event in office_events:
            day_dict[event.start_time.strftime("%A")].append(event)
        
        return day_dict

    def __str__(self):
        return f"'{self.title}', {self.start_time.strftime('%d %b at %H:%M')}"

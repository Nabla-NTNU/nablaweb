from django.db import models
from django.conf import settings # AUTH_USER_MODEL
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta

class OfficeEvent(models.Model):
    """Event in the office. Used as an internal calendar for office use."""

    start_time = models.DateTimeField(blank = False, help_text = "Reservasjoner mellom 11:00 og 13:00 krever styrets godkjenning.")
    end_time   = models.TimeField(blank = False)
    repeating  = models.BooleanField(blank = False, default = False)
    contact_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    public     = models.BooleanField(blank = False, default = False, help_text = "Synlig for alle, uten å logge inn")

    title = models.CharField(max_length = 30)
    description = models.TextField(blank = True)

    @property
    def duration(self):
        """Returns duration of event in seconds"""
        return datetime.combine(self.start_time.date(), self.end_time) - self.start_time # Hacky way of getting timedelta

    def duration_natural(self):
        """Return a natural language string with length of duration"""

        hours, minutes = self.duration.seconds/3600, (self.duration.seconds//60)%60

        if hours < 1:
            return f"{minutes} minutter"

        plural_suffix = '' if hours == 1 else 'r'
        return f"{hours:.1g} time{plural_suffix}"

    def clean(self):
        if self.start_time.time() >  self.end_time:
            raise ValidationError("start_time must be before end_time!")

    def get_office_event_week(only_public = False):
        """Returns a list officeEvents this weeks officeEvents
        Requires datetime"""

        now = datetime.now()

        end_of_week = now + timedelta(days = ( 6 - now.weekday() ))
        end_of_week = end_of_week.date()

        # Find events this week, but ignore those that have happened
        # Also include all repeating events
        office_events = OfficeEvent.objects.filter(models.Q(start_time__date__gte = now, start_time__date__lte = end_of_week)  | models.Q(repeating = True))

        if only_public:
            office_events = office_events.exclude(public = False)

        # We can not do database sort, because weekday is not a column
        office_events = sorted(office_events, key = lambda event: (event.start_time.weekday(), event.start_time.time()))        
        return office_events

    def __str__(self):
        return f"'{self.title}', {self.start_time.strftime('%d %b at %H:%M')}"

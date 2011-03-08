# arrangement/models.py

from django.db import models
from django.contrib.auth.models import User

EVENT_TYPES = {'simple':
                   {'short_description': 'Simple event',
                    'groups': [],
                    'extra_options': [],},
               'standard':
                   {'short_description': 'Standard event',
                    'groups': [],
                    'extra_options': [],},
               'bedpres':
                   {'short_description': 'Business presentation',
                    'groups': [],
                    'extra_options': [],},
               }

EVENT_CHOICES = ((event_type, info['short_description'])
                 for (event_type, info) in EVENT_TYPES.iteritems())

class Event(models.Model):
    """class Event(models.Model)"""

    class Meta:
        verbose_name_plural = "arrangement"
        permissions = (
            ("can_close", ""),
            )

    alternative_id = models.CharField(max_length=32, blank=True)
    event_type = models.CharField(max_length=32, choices=EVENT_CHOICES)

    title = models.CharField(max_length=80)
    summary = models.TextField(max_length=1000)
    body = models.TextField(max_length=5000)
#   image = models.ImageField(blank=True)

    location = models.CharField(max_length=80)
    event_start = models.DateTimeField(null=True)

    organizer = models.CharField(max_length=80, blank=True)

    is_only_for_nabla = models.NullBooleanField(default=False, blank=True)
    # TODO: Adgangskontroll basert paa klassetrinn

    places = models.PositiveIntegerField(null=True, blank=True)
    attending_users = models.ManyToManyField(User, related_name='events_attending+', null=True, blank=True)
    waiting_list = models.ManyToManyField(User, related_name='events_waiting+', null=True, blank=True)

    has_registration_deadline = models.NullBooleanField(default=False, blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)

    allow_deregistration = models.NullBooleanField(default=True, blank=True)
    deregistration_deadline = models.DateTimeField(null=True, blank=True)

    is_closed = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s, %s' % (self.title, self.event_start.strftime('%d/%m/%y'))

    def free_places(self):
        return self.places - len(self.attending_users.all())

    def is_full(self):
        return self.free_places() == 0

    def user_is_attending(self, user):
        return user in self.attending_users.all()

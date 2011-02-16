from django.db import models
from django.contrib.auth.models import User

# Dummy-klasse
class Nyhet(models.Model):
    """class Nyhet(models.Model)"""

    title = models.CharField(max_length=100)
    summary = models.TextField()
    body = models.TextField()


class Event(Nyhet):
    """class Event(Nyhet)"""

    class Meta:
        verbose_name_plural = "arrangement"

    location = models.CharField(max_length=100)
    time = models.DateTimeField()

    open_for_all = models.BooleanField(default=False) # for alle eller paamelding?
    places = models.PositiveIntegerField(default=0)
    registered = models.ManyToManyField(User)

    has_registration_deadline = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField()

    non_nabla = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s, %s" % (self.title[:20], self.time.strftime("%d/%m/%y"))

    def free_places(self):
        return self.places - len(self.registered.all())

from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    """
    class Event(models.Model)
    """

    class Meta:
        verbose_name_plural = "arrangement"
        permissions = (
            ("can_close", "")
            )

    title = models.CharField(max_length=100)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)

    location = models.CharField(max_length=100)
    time = models.DateTimeField()

    open_for_all = models.BooleanField(default=False)
    non_nabla = models.BooleanField(default=False)

    places = models.PositiveIntegerField(default=0)
    attending_users = models.ManyToManyField(User, blank=True)

    has_registration_deadline = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField(blank=True)
    allow_unregistration = models.BooleanField(default=True)

    closed = models.BooleanField(default=False)


    def __unicode__(self):
        return u'%s, %s' % (self.title, self.time.strftime('%d/%m/%y'))

    def free_places(self):
        return self.places - len(self.attending_users.all())

    def is_full(self):
        return self.open_for_all == False and self.free_places() == 0

    def user_is_attending(self, user):
        return user in self.attending_users.all()


class BedPres(Event):
    """
    class BedPres(Event)
    """

    class Meta:
        verbose_name_plural = "bedriftspresentasjoner"

    bpc_sync = models.BooleanField(default=False)
    bpc_id = models.IntegerField(blank=True)

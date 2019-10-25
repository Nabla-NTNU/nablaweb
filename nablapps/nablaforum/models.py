from django.db import models
from django.utils import timezone
from nablapps.accounts.models import NablaUser, NablaGroup

class Channel(models.Model):
    ''' Represents a channel in the forum '''
    group = models.ForeignKey(NablaGroup, on_delete=models.CASCADE, blank=True, null=True)
    members = models.ManyToManyField(NablaUser, related_name='members')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    is_feed = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    has_unreads = models.BooleanField(default=False)


    def __str__(self):
        return self.name


class Thread(models.Model):
    ''' Represents a thread in a channel'''
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE) #which channel it belongs to
    threadstarter = models.ForeignKey(NablaUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    has_unreads = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class Message(models.Model):
    ''' Represents a message in a thread '''
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(NablaUser, on_delete=models.CASCADE,)
    message = models.TextField()
    read_by_user = models.ManyToManyField(NablaUser, related_name="read_by_user")
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """Update created timestamp on creation"""
        if not self.id:  # Does not exist yet, ie. creation not modification
            self.created = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username



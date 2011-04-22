# innhold/models.py

from django.db import models
from django.contrib.auth.models import User
import datetime

class SiteContent(models.Model):
    class Meta:
        abstract = True

    created_date = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, related_name="%(class)s_created", editable=False, blank=False, null=True)
    last_changed_date = models.DateTimeField(auto_now=True, null=True)
    last_changed_by = models.ForeignKey(User, related_name="%(class)s_edited", editable=False, blank=True, null=True)

    headline = models.CharField(max_length=100, blank=False)
    lead_paragraph = models.TextField(blank=True)
    body = models.TextField(blank=True)

    def __unicode__(self):
        return self.headline

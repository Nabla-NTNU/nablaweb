from django.db import models
from django.contrib.auth.models import User
import datetime

class SiteContent(models.Model):
    class Meta:
        abstract = True

    created_date = models.DateTimeField(default=datetime.datetime.now(), blank=False, null=True)
    created_by = models.ForeignKey(User, related_name="%(class)s_created", blank=False, null=True)
    last_changed_date = models.DateTimeField(blank=True, null=True)
    last_changed_by = models.ForeignKey(User, related_name="%(class)s_edited", blank=True, null=True)

    headline = models.CharField(max_length=100, blank=False)
    lead_paragraph = models.TextField(blank=True)
    body = models.TextField(blank=True)

class News(SiteContent):
    class Meta:
        verbose_name_plural = "news"
    
    def __unicode__(self):
        return self.headline

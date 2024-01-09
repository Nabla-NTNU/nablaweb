from django.contrib import admin

# Register your models here.
from .models import Subscription, MailFeed

admin.site.register(Subscription)
admin.site.register(MailFeed)

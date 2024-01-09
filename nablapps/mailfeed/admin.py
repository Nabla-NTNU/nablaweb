from django.contrib import admin

# Register your models here.
from .models import Subscription, Mailfeed

admin.site.register(Subscription)
admin.site.register(Mailfeed)

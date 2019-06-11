from django.contrib import admin

# Register your models here.
from .models import QrEvent, QrTicket

admin.site.register(QrEvent)
admin.site.register(QrTicket)

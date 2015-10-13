from django.contrib import admin
from .models import AdventCalendar, AdventDoor


class AdventDoorInline(admin.TabularInline):
    model = AdventDoor
    extra = 24
    fields = ('number', 'content', 'template')
    fk_name = "calendar"


class AdventCalendarAdmin(admin.ModelAdmin):
    inlines = [AdventDoorInline]

    class Meta:
        verbose_name = "Julekalender"
        verbose_name_plural = "Julekalendere"
        fields = '__all__'

admin.site.register(AdventCalendar, AdventCalendarAdmin)

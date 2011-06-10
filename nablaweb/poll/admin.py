from polls.models import Poll
from django.contrib import admin

class ChoiceInline(admin.TabularInline)
    model = Choice
    extra = 5

class PollAdmin(admin.ModelAdmin):
    fields = ['publication_date', 'question', 'creation_date', 'edit_date']
    list_display = ('question', 'publication_date', 'creation_date', 'edit_date')
    list_filter = ['publication_date']
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)

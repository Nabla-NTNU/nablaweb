# -*- coding: utf-8 -*-

from poll.models import Poll, Choice
from django.contrib import admin

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 5
    fields = ('choice', 'votes', )

class PollAdmin(admin.ModelAdmin):
    fields = ['publication_date', 'question', 'is_current', 'users_voted', ]
    readonly_fields = ['users_voted', ]
    list_display = ('question', 'publication_date', 'is_current')
    list_filter = ['publication_date']
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)

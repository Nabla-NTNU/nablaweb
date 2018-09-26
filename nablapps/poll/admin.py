"""
Admin interface for poll app.
"""
from django.contrib import admin
from .models import Poll, Choice


class ChoiceInline(admin.TabularInline):
    """Define how the choices should be viewed inlined with the poll"""
    model = Choice
    extra = 5
    fields = ('choice', 'votes', )
    fk_name = "poll"


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    """Admin interface for poll model"""
    fields = ['publication_date', 'question', 'answer', 'is_current', 'users_voted', ]
    readonly_fields = ['users_voted', 'created_by']
    list_display = ('question', 'publication_date', 'is_current', 'created_by')
    list_filter = ['publication_date']
    inlines = [ChoiceInline]
    actions = ['make_current']

    def make_current(self, request, queryset):
        """Admin action to make a (single) poll the current poll"""
        if queryset.count != 1:
            self.message_user(request, "Only one can be marked as the current poll!")

        Poll.objects.filter(is_current=True).update(is_current=False)
        queryset.update(is_current=True)
    make_current.short_description = "Gjør til forsideavstemning"

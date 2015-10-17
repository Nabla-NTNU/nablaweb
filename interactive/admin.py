from django.contrib import admin
from .models import AdventCalendar, AdventDoor, Quiz, QuizQuestion


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


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 8
    fields = ('question', 'alternative_1', 'alternative_2', 'alternative_3', 'alternative_4', 'correct_alternative')
    fk_name = "quiz"


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizQuestionInline]
    exclude = ['scoreboard']

    class Meta:
        verbose_name = "Quiz"

admin.site.register(AdventCalendar, AdventCalendarAdmin)
admin.site.register(Quiz, QuizAdmin)

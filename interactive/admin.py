from django.contrib import admin
from .models import AdventCalendar, AdventDoor, Quiz, QuizQuestion, Test, TestQuestion, TestQuestionAlternative, TestResult


class AdventDoorInline(admin.TabularInline):
    model = AdventDoor
    extra = 24
    fields = ('number', 'content', 'short_description', 'is_lottery', 'template', 'image', 'is_text_response', 'winner',
              'quiz')
    readonly_fields = ['winner']
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


class TestQuestionAlternativeInline(admin.TabularInline):
    model = TestQuestionAlternative
    fields = ['text']
    fk_name = "question"


class TestQuestionInline(admin.TabularInline):
    model = TestQuestion
    inlines = [TestQuestionAlternativeInline]
    fields = ['text']
    fk_name = "test"


class TestResultInline(admin.TabularInline):
    model = TestResult
    fields = ('title', 'content')
    fk_name = "test"


class TestAdmin(admin.ModelAdmin):
    inlines = [TestQuestionInline, TestResultInline]

    class Meta:
        verbose_name = "Brukertest"


admin.site.register(AdventCalendar, AdventCalendarAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Test, TestAdmin)

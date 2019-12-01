from django import forms
from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea

from .models.code_golf import CodeTask, Result
from .models import (
    AdventCalendar,
    AdventDoor,
    Quiz,
    QuizQuestion,
    Test,
    TestResult,
    TestQuestion,
    TestQuestionAlternative,
    ColorChoice
)
from .models.advent import Santa


class AdventDoorInline(admin.TabularInline):
    model = AdventDoor
    extra = 24
    fields = (
        'number',
        'content',
        'short_description',
        'is_lottery',
        'template',
        'image',
        'is_text_response',
        'winner',
        'quiz',
        'user_test',
    )
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
    fields = (
        'question',
        'alternative_1',
        'alternative_2',
        'alternative_3',
        'alternative_4',
        'correct_alternative',
    )
    fk_name = "quiz"


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizQuestionInline]
    exclude = ['scoreboard']

    class Meta:
        verbose_name = "Quiz"


class TestQuestionAlternativeForm(forms.ModelForm):

    class Meta:
        model = TestQuestionAlternative
        fields = ['target']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['target'].queryset = TestResult.objects.filter(
                                        test=self.instance.question.test)


class TestQuestionAlternativeInline(admin.TabularInline):
    model = TestQuestionAlternative
    fields = ('text', 'target', 'weights', )
    fk_name = "question"
    extra = 1
    form = TestQuestionAlternativeForm
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 1,
                   'cols': 10,
                   'style': 'height: 4em;'})},
    }


class TestQuestionAdmin(admin.ModelAdmin):
    inlines = [TestQuestionAlternativeInline]
    exclude = ('test',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 1,
                   'cols': 10,
                   'style': 'height: 4em;'})},
    }

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class TestQuestionInline(admin.TabularInline):
    model = TestQuestion
    extra = 1
    fields = ('text', 'changeform_link')
    fk_name = "test"
    readonly_fields = ('changeform_link',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 1,
                   'cols': 10,
                   'style': 'height: 4em;'})},
    }


class TestResultInline(admin.TabularInline):
    model = TestResult
    fields = ('title', 'content')
    fk_name = "test"
    extra = 1


class TestAdmin(admin.ModelAdmin):
    inlines = [TestQuestionInline, TestResultInline]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 1,
                   'cols': 10,
                   'style': 'height: 4em;'})},
    }

    
admin.site.register(AdventCalendar, AdventCalendarAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestQuestion, TestQuestionAdmin)
admin.site.register(CodeTask)
admin.site.register(Result)
admin.site.register(Santa)
admin.site.register(ColorChoice)

from django.forms import (BaseFormSet, HiddenInput, ModelForm, Textarea, TextInput,
                          formset_factory, ValidationError)
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import FormView

from .models import Application, ApplicationRound, Committee

class BaseApplicationFormSet(BaseFormSet):
    def clean(self):
        """Make sure that there is a first priority"""
        super().clean()
        first_form = self.forms[0]
        if ("committee" not in first_form.cleaned_data or
            first_form.cleaned_data["committee"] is None):
            raise ValidationError("You mus set a first priority!")

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ["application_round", "applicant", "priority"]
        widgets = {
            "application_text": TextInput(),
        }

    def __init__(self, *args, application_round, applicant, **kwargs):
        super().__init__(*args, **kwargs)
        self.application_round = application_round
        self.applicant = applicant
        self.fields["committee"].required = False

    # def full_clean(self):
    #     super().full_clean()
    #     self.instance.applicant = self.applicant
    #     self.instance.application_round = self.application_round
    #     try:
    #         self.instance.validate_unique()
    #     except ValidationError as e:
    #         self._update_errors(e)

        # The ideal would be to call validate_unique, but as of now
        # it would raise an error if we tried to update an existing
        # instance.

        # try:
        #     self.instance.validate_unique()
        # except ValidationError as e:
        #     self._update_errors(e)

class ApplicationView(FormView):
    form_class = formset_factory(ApplicationForm, extra=2, formset=BaseApplicationFormSet)
    template_name = "apply_committee/apply.html"

    def setup(self, request, *args, **kwargs):
        self.application_round = ApplicationRound.get_current()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return Application.objects.filter(
            applicant=self.request.user,
            application_round=self.application_round
        )

    def get_initial(self):
        existing = self.get_queryset().order_by("priority")
        initial = []
        for entry in existing:
            initial.append({
                "committee": entry.committee,
                "application_text": entry.application_text,
                "anonymous": entry.anonymous
            })
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['form_kwargs'] = {
            'applicant': self.request.user,
            'application_round': self.application_round
            }
        return kwargs

    def form_valid(self, formset):
        Application.objects.filter(
            applicant=self.request.user,
            application_round=self.application_round
        ).delete()

        priority = 0
        for form in formset:
            if ("committee" in form.cleaned_data and
                form.cleaned_data["committee"] is not None):
                priority+=1
                application = form.save(commit=False)
                application.priority = priority
                application.applicant = self.request.user
                application.application_round = self.application_round
                application.save()

        # Redirect back to form when submitted
        # TODO: create confirm page instead?
        return redirect("apply-committee")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application_round"] = self.application_round
        context["formset"] = context.pop("form", None)  # Give a more intuitive name
        return context

class ApplicationListView(ListView):
    model = Application
    context_object_name = "application_list"

    def get_queryset(self):
        return self.model.objects.\
            filter(application_round=ApplicationRound.get_current()).\
            order_by("committee")

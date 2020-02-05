from django.forms import (BaseFormSet, HiddenInput, ModelForm, Textarea, TextInput,
                          formset_factory, ValidationError)
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from .models import Application, ApplicationRound, Committee

class BaseApplicationFormSet(BaseFormSet):
    def clean(self):
        """Make sure that there is a first priority"""
        first_form = self.forms[0]
        if first_form.cleaned_data["committee"] is None:
            raise ValidationError("You mus set a first priority!")

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ["application_round", "applicant"]
        widgets = {
            "application_text": TextInput(),
            "priority": HiddenInput(),
        }

    def __init__(self, *args, application_round, applicant, is_update=False, **kwargs):
        self.application_round = application_round
        self.applicant = applicant
        self.is_update = is_update
        super().__init__(*args, **kwargs)
        self.fields["committee"].required = False

    def full_clean(self):
        super().full_clean()
        self.instance.applicant = self.applicant
        self.instance.application_round = self.application_round

        # The ideal would be to call validate_unique, but as of now
        # it would raise an error if we tried to update an existing
        # instance.

        # try:
        #     self.instance.validate_unique()
        # except ValidationError as e:
        #     self._update_errors(e)

class ApplicationView(FormView):
    form_class = formset_factory(ApplicationForm, extra=0, formset=BaseApplicationFormSet)
    template_name = "apply_committee/apply.html"
    num_initial = 3  # Inital number of options

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
                "priority": entry.priority,
                "committee": entry.committee,
                "application_text": entry.application_text,
                "anonymous": entry.anonymous
            })

        for i in range(len(initial), self.num_initial):
            initial.append({"priority": i+1})
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # existing = self.get_queryset()
        # initial = kwargs["initial"]
        # for i, entry in enumerate(existing):
        #     initial[i]["priority"] = entry.priority
        #     initial[i]["committee"] = entry.committee
        #     initial[i]["application_text"] = entry.application_text
        #     initial[i]["anonymous"] = entry.anonymous

        # initial = sorted(initial, key=lambda item: item["priority"])
        # kwargs["initial"] = initial

        # form_kwargs are passed by formset to the underlying form
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

        for form in formset:
            committee = form.cleaned_data["committee"]
            print(committee)
            if committee is not None:
                application = form.save(commit=False)
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

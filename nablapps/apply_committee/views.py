import csv
import logging
import re

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import (
    BaseFormSet,
    ModelForm,
    TextInput,
    ValidationError,
    formset_factory,
)
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView

from nablapps.accounts.models import NablaGroup
from nablapps.com.views import CommitteeOverview
from nablapps.core.templatetags.listutil import row_split

from .models import Application, ApplicationRound, Committee


class BaseApplicationFormSet(BaseFormSet):
    def clean(self):
        super().clean()

        # Make sure there is a first form
        first_form = self.forms[0]
        if (
            "committee" not in first_form.cleaned_data
            or first_form.cleaned_data["committee"] is None
        ):
            raise ValidationError("You mus set a first priority!")

        # Check that the same committee is not selected twice
        committees = []
        for form in self.forms:
            if (
                "committee" not in form.cleaned_data
                or form.cleaned_data["committee"] is None
            ):
                continue
            committee = form.cleaned_data["committee"]
            if committee in committees:
                raise ValidationError("You cannot select the same committee twice!")
            committees.append(committee)


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ["application_round", "applicant", "priority"]
        widgets = {
            "application_text": TextInput(attrs={"placeholder": "Fritekst/Instrument"}),
        }

        labels = {
            "committee": "Komité",
            "application_text": "Fritekst",
            "anonymous": "Anonym søknad",
        }

        help_texts = {
            "anonymous": None,  # Do not show help text
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


class ApplicationView(LoginRequiredMixin, FormView):
    form_class = formset_factory(
        ApplicationForm, extra=2, formset=BaseApplicationFormSet
    )
    template_name = "apply_committee/apply.html"
    success_url = "confirmation/"

    def __init__(self, *args, **kwargs):
        self.application_round = ApplicationRound.get_current()
        return super().__init__(*args, **kwargs)

    def get_queryset(self):
        return Application.objects.filter(
            applicant=self.request.user, application_round=self.application_round
        )

    def get_initial(self):
        existing = self.get_queryset().order_by("priority")
        initial = []
        for entry in existing:
            initial.append(
                {
                    "committee": entry.committee,
                    "application_text": entry.application_text,
                    "anonymous": entry.anonymous,
                }
            )
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["form_kwargs"] = {
            "applicant": self.request.user,
            "application_round": self.application_round,
        }
        return kwargs

    def form_valid(self, formset):
        Application.objects.filter(
            applicant=self.request.user, application_round=self.application_round
        ).delete()

        priority = 0
        for form in formset:
            if (
                "committee" in form.cleaned_data
                and form.cleaned_data["committee"] is not None
            ):
                priority += 1
                application = form.save(commit=False)
                application.priority = priority
                application.applicant = self.request.user
                application.application_round = self.application_round
                application.save()

        return super().form_valid(formset)
        # Redirect back to form when submitted
        # TODO: create confirm page instead?
        return redirect("apply-committee")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application_round"] = self.application_round
        context["formset"] = context.pop("form", None)  # Give a more intuitive name
        return context


class BaseApplicationListView(ListView):
    model = Application
    context_object_name = "application_list"

    def get_context_data(self):
        context = super().get_context_data()
        context["application_round"] = ApplicationRound.get_current()
        return context

    def get_queryset(self):
        applications = self.model.objects.filter(
            application_round=ApplicationRound.get_current()
        )
        committees = {}
        for application in applications:
            committees[application.committee] = committees.get(
                application.committee, []
            )
            committees[application.committee].append(application)
        return committees


class AdminApplicationListView(UserPassesTestMixin, BaseApplicationListView):
    template_name = "apply_committee/admin_application_list.html"

    def test_func(self):
        try:
            admin_group = NablaGroup.objects.get(name="Gruppeledere")
        except NablaGroup.DoesNotExist:
            logging.getLogger("django").error(
                "No NablaGroup 'Gruppeledere'. This is unexpected."
            )
            return False

        # This might seem like a roundabout way, but remember
        # that this is a database operation. That is faster than f.eks.
        # (pseudo-code) admin_group in user.groups
        return self.request.user.groups.filter(pk=admin_group.pk).exists()


class ConfirmView(LoginRequiredMixin, TemplateView):
    template_name = "apply_committee/confirm.html"

    def get_context_data(self):
        applications = Application.objects.filter(
            application_round=ApplicationRound.get_current(),
            applicant=self.request.user,
        ).order_by("priority")
        context = super().get_context_data()
        context["applications"] = applications
        return context


@staff_member_required
def generate_csv(http_request):
    response = HttpResponse(content_type="text/csv", charset="latin-1")
    response["Content-Disposition"] = 'attachment; filename="export.csv"'

    writer = csv.writer(response, dialect="excel")

    current_application_round = ApplicationRound.get_current()
    committees = list(BaseApplicationListView().get_queryset().keys())

    table = list()
    applicants = list()
    applicant_texts = list()
    top_row = list(["Nr", "Navn"])

    for application in current_application_round.get_applicants():
        if application.applicant not in applicants:
            applicants.append(application.applicant)

    for applicant in applicants:
        row = list()
        applicant_text = list()
        row.append(len(table) + 1)  # Row index
        row.append(f"{applicant.first_name} {applicant.last_name}")

        applications = Application.objects.filter(
            application_round=ApplicationRound.get_current(),
            applicant=applicant,
        ).order_by("priority")

        for application in applications:
            row.append(application.committee)
            if application.application_text:
                applicant_text.append(
                    f"{application.committee}: {application.application_text}"
                )

        while len(top_row) < len(row):
            top_row.append(f"{len(top_row) - 1}. valg")

        applicant_texts.append(applicant_text)
        table.append(
            row + [""] * (len(committees) - len(applications) + 1)
        )  # Need blanks to fill in applicant texts later

    for i in range(len(table)):
        table[i][len(top_row)] = ", ".join(applicant_texts[i])

    writer.writerow(top_row + ["Tekst", "Krangel?"] + committees + ["Trukket"])
    writer.writerows(table)

    return response

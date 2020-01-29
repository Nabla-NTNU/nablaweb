from django.views.generic.edit import FormView
from django.forms import ModelForm, Textarea, TextInput, formset_factory

from .models import Application, ApplicationRound, Committee


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ["application_round", "applicant"]
        widgets = {
            "application_text": TextInput(),
        }


class ApplicationView(FormView):
    form_class = formset_factory(ApplicationForm, extra=3)
    template_name = "apply_committee/apply.html"

    def form_valid(self, form):
        # Redirect back to form when submitted
        # TODO: create confirm page instead?
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application_round = ApplicationRound.get_current()
        if application_round is None:
            context["form"] = None
            return context

        context["application_round"] = application_round
        return context

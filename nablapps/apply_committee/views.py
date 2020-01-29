from django.forms import (HiddenInput, ModelForm, Textarea, TextInput,
                          formset_factory)
from django.views.generic.edit import FormView

from .models import Application, ApplicationRound, Committee


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        exclude = ["application_round", "applicant"]
        widgets = {
            "application_text": TextInput(),
            "priority": HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["committee"].required = False


class ApplicationView(FormView):
    num_forms = 3  # Number of forms in formset
    form_class = formset_factory(ApplicationForm, extra=0)
    template_name = "apply_committee/apply.html"
    initial = [{"priority": i+1} for i in range(num_forms)]

    def setup(self, request, *args, **kwargs):
        print("setup")
        return super().setup(request, *args, **kwargs)
        print("setup!!!!!!!!")
        self.application_round = ApplicationRound.get_current()

    def form_valid(self, formset):
        for form in formset:
            committee = form.cleaned_data["committee"]
            if committee is not None:
                application = form.save(commit=False)
                application.applicant = self.request.user
                application.application_round = self.application_round
                application.save()

        # Redirect back to form when submitted
        # TODO: create confirm page instead?
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
#        application_round = ApplicationRound.get_current()
        context["application_round"] = self.application_round
        context["formset"] = context.pop("form", None)  # Give a more intuitive name
        return context

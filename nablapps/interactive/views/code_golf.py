from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.functions import Concat
from django.forms import CharField, HiddenInput, ModelForm, Textarea
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from ..models.code_golf import CodeTask, Result


class ResultForm(ModelForm):
    """Form for submitting code.

    Discussion:
        We cannot verify that the user's code actually outputs what he reports, but
        we might at the very least verify that they include the correct output in
        their response. We here extend the model form of the Result model to include
        a field `output`, and verify that that field has the correct output (which
        is passed to the form through the constructor).
        Whether this is actually useful, or if a simple client side check is sufficient,
        can be discussed. Future refactorings of code golf are free to remvoe this
        server side check if they wish, which will have the benefit of making the
        code simpler.
    """

    output = CharField(
        widget=HiddenInput(attrs={"v-model": "output"})
    )  # The ouput of the user's code

    def __init__(self, *args, **kwargs):
        self.task = kwargs.pop("task")
        super().__init__(*args, **kwargs)

    class Meta:
        model = Result
        fields = ["solution"]
        labels = {
            "solution": "",  # Drop the label
        }
        widgets = {
            "solution": Textarea(
                attrs={"placeholder": "Your solution", "v-model": "user_code"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        output = cleaned_data.get("output")
        if output != self.task.correct_output:
            raise ValidationError("Output does not match correct output")


class CodeGolf(LoginRequiredMixin, CreateView):
    """View for writing and submitting solutions"""

    model = Result
    form_class = ResultForm
    template_name = "interactive/code_golf.html"

    def get_success_url(self):
        return reverse("code_golf_score", kwargs={"task_id": self.task.id})

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(CodeTask, pk=self.kwargs.get("task_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["task"] = self.task
        # kwargs["auto_id"] = False
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.task
        context["result_list"] = Result.objects.best_by_user(task=self.task).order_by(
            "length"
        )
        return context

    def form_valid(self, form):
        """Set other fields"""
        form.instance.user = self.request.user
        form.instance.task = self.task
        form.instance.python_version = (
            "python2.7"  # NB! Change if changing Skulpt version
        )
        return super().form_valid(form)


def markdownify_code(code):
    """
    Takes a code as a string and converts it to a form where it will be
    formatted correctly by markdown.

    As of now, it is to add tabs in front of each line, but this is not very pretty...
    """

    return "\n".join(["\t" + line for line in code.split("\n")])


@login_required
def code_golf_score(request, task_id):
    """
    Show user list with number of chars for their code.
    If user is logged in show users solution, if not, only show the results list.
    """

    task = get_object_or_404(CodeTask, pk=task_id)
    result_list = Result.objects.best_by_user(task=task).order_by("length")

    output = markdownify_code(task.correct_output)

    context = {"output": output, "result_list": result_list, "task": task}

    user_has_solution = Result.objects.filter(user=request.user, task=task).exists()
    context["has_solution"] = user_has_solution

    if user_has_solution:
        user_results = Result.objects.filter(user=request.user, task=task).order_by(
            "length"
        )
        best_result = user_results.first()
        length = best_result.length
        code = best_result.solution  # Add #!python for markdown
        context["code"] = code
        context["length"] = length
        context["user_results"] = user_results

    return render(request, "interactive/code_golf_score.html", context)


class CodeTaskListView(ListView):
    model = CodeTask

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        task_list = CodeTask.objects.prefetch_related("result_set").order_by("-pk")
        best_results = []
        user_results = []

        for obj in task_list:
            best_results.append(obj.get_best_result)
            if self.request.user.is_authenticated:
                user_result = (
                    obj.result_set.filter(user=self.request.user)
                    .order_by("length")
                    .first()
                )
                if user_result is not None:
                    user_results.append(user_result.length)
                else:
                    user_results.append("--")
            else:
                user_results.append("--")

        tasks = zip(task_list, best_results, user_results)
        newest_task = task_list.first()

        context["newest_task"] = newest_task
        context["tasks"] = tasks
        return context

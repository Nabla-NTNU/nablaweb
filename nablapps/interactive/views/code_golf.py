from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.functions import Concat
from django.forms import CharField, HiddenInput, ModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from ..forms.code_golf import CodeGolfForm
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

    output = CharField(widget=HiddenInput)  # The ouput of the user's code

    def __init__(self, *args, **kwargs):
        self.task = kwargs.pop("task")
        super().__init__(*args, **kwargs)

    class Meta:
        model = Result
        fields = ["solution"]

    def clean(self):
        cleaned_data = super().clean()
        output = cleaned_data.get("output")
        if output != self.task.correct_output:
            raise ValidationError("Output does not match correct output")


class CodeGolf2(LoginRequiredMixin, CreateView):
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
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.task
        context["result_list"] = Result.objects.best_by_user(full_object=True)
        print(context["result_list"])
        return context

    def form_valid(self, form):
        """Set other fields"""
        form.instance.user = self.request.user
        form.instance.task = self.task
        return super().form_valid(form)


class CodeGolf(LoginRequiredMixin, View):
    def get(self, request, task_id):
        # Display code task
        task = get_object_or_404(CodeTask, pk=task_id)
        task_text = task.task
        code_golf_form = CodeGolfForm()
        result_list = task.result_set.all()
        # Cannot use .sorted_by since length is a property, not a db field
        sorted_result_list = sorted(
            result_list, key=lambda result: (result.length, result.submitted_at)
        )
        context = {
            "task": task,
            "code_golf_form": code_golf_form,
            "task_text": task_text,
            "result_list": sorted_result_list,
        }
        return render(request, "interactive/code_golf.html", context)

    def post(self, request, task_id):
        submitted_at = timezone.now()

        # Submit output, check answer and count length
        form = CodeGolfForm(request.POST)

        if not form.is_valid():
            return HttpResponse(
                'Oi, noe gikk galt. Husk å trykke "run", og sjekk at koden skriver ut noe før du trykker send!'
            )

        code = form.get_submitted_code()
        output = form.get_submitted_output()
        task = get_object_or_404(CodeTask, pk=task_id)
        correct_output = task.correct_output

        """
        We cannot know if the user has sent a code that matches the output they
        say that they got. The best we can do is to verify the output sent in the request.
        """

        if output != correct_output:
            correct = str(correct_output)
            context = {"correct": correct, "output": output, "task_id": task_id}
            return render(request, "interactive/code_golf_error.html", context)

        score = Result.compute_length(code)

        try:
            previous_result = Result.objects.get(user=request.user, task=task)
        except Result.DoesNotExist:
            new_best_score = True
            store_new_code = True
        else:
            new_best_score = score < previous_result.length
            store_new_code = score <= previous_result.length

        updates = {}

        if store_new_code:
            # The user has tied (or better) their old score -> update the stored code
            updates["solution"] = code

            if new_best_score:
                # The user has achieved a new best score -> update the submission time
                updates["submitted_at"] = submitted_at

        Result.objects.update_or_create(
            user=request.user,
            task=task,
            defaults=updates,
        )

        return redirect("/kodegolf/score/" + str(task_id))


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
    result_list = task.result_set.all()

    output = markdownify_code(task.correct_output)

    context = {"output": output, "result_list": result_list}

    user_result = result_list.filter(user=request.user).first()
    user_has_solution = user_result is not None

    context["has_solution"] = user_has_solution

    if user_has_solution:
        user_results = (
            Result.objects.with_length().filter(user=request.user).order_by("length")
        )
        best_result = user_results.first()
        length = best_result.length
        code = best_result.solution  # Add #!python for markdown
        code = markdownify_code(code)
        context["code"] = code
        context["length"] = length
        context["user_results"] = user_results

    return render(request, "interactive/code_golf_score.html", context)


class CodeTaskListView(ListView):
    model = CodeTask

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        task_list = CodeTask.objects.all()
        best_results = []
        user_results = []

        for obj in task_list:
            best_results.append(obj.get_best_result)
            if self.request.user.is_authenticated:
                try:
                    user_results.append(
                        obj.result_set.get(user=self.request.user).length
                    )
                except ObjectDoesNotExist:
                    user_results.append("--")
            else:
                user_results.append("--")

        tasks = zip(task_list, best_results, user_results)
        newest_task = task_list.first()

        context["newest_task"] = newest_task
        context["tasks"] = tasks
        return context

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.list import ListView

from ..forms.code_golf import CodeGolfForm
from ..models.code_golf import CodeTask, Result


class CodeGolf(LoginRequiredMixin, View):
    def get(self, request, task_id):
        # Display code task
        task = get_object_or_404(CodeTask, pk=task_id)
        task_text = task.task
        code_golf_form = CodeGolfForm()
        result_list = task.result_set.all()
        # Cannot use .sorted_by since length is a property, not a db field
        sorted_result_list = sorted(result_list, key=lambda x: x.length)
        context = {
            "task": task,
            "code_golf_form": code_golf_form,
            "task_text": task_text,
            "result_list": sorted_result_list,
        }
        return render(request, "interactive/code_golf.html", context)

    def post(self, request, task_id):
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

        # Only one result per user
        Result.objects.update_or_create(
            user=request.user, task=task, defaults={"solution": code,},
        )

        return redirect("/kodegolf/score/" + str(task_id))


def markdownify_code(code):
    """
    Takes a code as a string and converts it to a form where it will be
    formatted correctly by markdown.

    As of now, it is to add tabs in front of each line, but this is not very pretty...
    """

    return "\n".join(["\t" + line for line in code.split("\n")])


def code_golf_score(request, task_id):
    """
    Show user list with number of chars for their code.
    If user is logged in show users solution, if not, only show the results list.
    """

    task = get_object_or_404(CodeTask, pk=task_id)
    result_list = task.result_set.all()
    # Cannot use .sorted_by since length is a property, not a db field
    sorted_result_list = sorted(result_list, key=lambda x: x.length)

    output = task.correct_output
    output = markdownify_code(output)

    context = {"output": output, "result_list": sorted_result_list}

    # True if the user has a solution, false if not
    try:
        user_has_solution = result_list.filter(user=request.user).exists
        print(user_has_solution)
    except Exception as e:
        print(e)
        user_has_solution = False  # If user is anonymous

    context["has_solution"] = user_has_solution

    if user_has_solution:
        user_result = result_list.get(user=request.user)
        length = user_result.length
        code = user_result.solution  # Add #!python for markdown
        code = markdownify_code(code)
        context["code"] = code
        context["length"] = length

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

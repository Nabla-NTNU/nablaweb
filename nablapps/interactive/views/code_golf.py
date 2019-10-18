from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from ..models.code_golf import CodeTask, Result
from ..forms.code_golf import CodeGolfForm


class CodeGolf(LoginRequiredMixin ,View):
    def get(self, request, task_id):
        # Display code task
        task = get_object_or_404(CodeTask, pk=task_id)
        task_text = task.task
        code_golf_form = CodeGolfForm()
        result_list = task.result_set.all()
        # Cannot use .sorted_by since length is a property, not a db field
        sorted_result_list = sorted(result_list, key=lambda x: x.length) 
        context = {'task': task,
                    'code_golf_form': code_golf_form,
                    'task_text': task_text,
                    'result_list': sorted_result_list,}
        return render(request, 'interactive/code_golf.html', context)

    def post(self, request, task_id):
        # Submit output, check answer and count length
        form = CodeGolfForm(request.POST)
        
        if not form.is_valid():
            return HttpResponse('Oi, noe gikk galt. Husk å trykke "run", og sjekk at koden skriver ut noe før du trykker send!')
        
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
            context = {'correct': correct, 'output': output, 'task_id': task_id}
            return render(request, 'interactive/code_golf_error.html', context)
            
        # Only one result per user
        Result.objects.update_or_create(
            user = request.user,
            task = task,
            defaults = {'solution': code,},
        )

        return redirect('/kodegolf/score/'+str(task_id))
        
def markdownify_code(code):
    """
    Takes a code as a string and converts it to a form where it will be 
    formatted correctly by markdown.

    As of now, it is to add tabs in front of each line, but this is not very pretty...
    """

    return "\n".join(["\t" + l for l in code.split("\n")])
    
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
    
    context = {'output': output, 'result_list': sorted_result_list}

    # True if the user has a solution, false if not
    try:
        user_has_solution = result_list.filter(user=request.user).exists
        print(user_has_solution)
    except Exception as e: 
        print(e)
        user_has_solution = False # If user is anonymous
        
    context['has_solution'] = user_has_solution
        
    if user_has_solution:
        user_result = result_list.get(user=request.user)
        length = user_result.length
        code = user_result.solution # Add #!python for markdown
        code = markdownify_code(code)
        context['code'] = code
        context['length'] = length
        
    return render(request, 'interactive/code_golf_score.html', context)

class CodeTaskListView(ListView):
    model = CodeTask
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result_list = Result.objects.all()
        sorted_result_list = sorted(result_list, key=lambda x: x.length) 
        best_result = sorted_result_list[0]
        user_result = result_list.get(user = self.request.user)

        newest_task = CodeTask.objects.all().reverse()[0]

        context["best_result"] = best_result
        context["user_result"] = user_result
        context["newest_task"] = newest_task
        return context

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.exceptions import ValidationError

from ..models.code_golf import CodeTask, Result
from ..forms.code_golf import Code_golf_form


class code_golf(View):
    def get(self, request, task_id):
        #display code task and fillout form
        task = get_object_or_404(CodeTask, pk=task_id)
        task_text = task.task
        code_golf_form = Code_golf_form()
        context = {'task': task, 'code_golf_form': code_golf_form, 'task_text': task_text}
        return render(request, 'interactive/code_golf.html', context)

    def post(self, request, task_id):
        #submit output, check answer and count length
        form = Code_golf_form(request.POST)
        if form.is_valid():
            code = form.get_submitted_code()
            output = form.get_submitted_output()
            task = get_object_or_404(CodeTask, pk=task_id)
            correct_output = task.correct_output

            length = len(code.split())
            user = request.user.get_full_name()
            result = task.result_set
            result.create(user=user, length=length)

            request.session['code'] = code
            request.session['output'] = output
            #request.session['length'] = length

            if output == correct_output:
                return redirect('/kodegolf/score/'+str(task_id))
            else:
                output = 'Beklager, feil output. Riktig svar er: ' + str(correct_output) + '. Ditt svar: ' + output
                context = {'output': output, 'task_id': task_id}
                return render(request, 'interactive/code_golf_error.html', context)

        else:
            return HttpResponse('Oi, noe gikk galt. Husk å trykke "run" før du trykker send!')
            

def code_golf_score(request, task_id):
    code = request.session['code']
    output = request.session['output'] 
    #length = request.session['length']
       
    task = get_object_or_404(CodeTask, pk=task_id)
    result_list = task.result_set.order_by('length')
    length = len(code.split())
    context = {'code': code, 'output': output, 'result_list': result_list, 'length': length,}

    return render(request, 'interactive/code_golf_score.html', context)


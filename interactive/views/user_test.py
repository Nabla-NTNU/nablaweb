from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from ..models.user_test import Test


class TestView(DetailView):
    model = Test
    template_name = "interactive/user_test.html"

    def get_form_url(self):
        return reverse('test_result', kwargs={'pk': self.object.id})


def test_result(request, pk):
    test = get_object_or_404(Test, id=pk)
    questions = test.questions.all()
    format_string = "{}_alternative"
    answers = (request.POST.get(format_string.format(q.id)) for q in questions)
    q_and_a = [
        (q, int(answer))
        for q, answer in zip(questions, answers)
        if answer is not None
        ]
    weighted_res = [q.alternatives.all()[a].get_target_with_weights() for q, a in q_and_a]
    scores = []
    results = test.results.all()
    for res in results:
        s = 0
        for ws in weighted_res:
            for w in ws:
                if res in w:
                    s += w[1]
        scores.append(s)
    max_score = max(scores)
    index = scores.index(max_score)
    result = results[index]
    context = {
        'base_template': test.template,
        'title': result.title,
        'content': result.content
    }
    return TemplateResponse(request,
                            'interactive/user_test_result.html',
                            context)

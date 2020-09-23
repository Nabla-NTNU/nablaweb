from collections import Counter
from itertools import chain

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import DetailView

from ..models.user_test import Test


class TestView(DetailView):
    model = Test
    template_name = "interactive/user_test.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=None)
        if obj.published or self.request.user.has_perm("interactive.change_test"):
            return obj
        else:
            raise Http404("Ikke publisert")

    def get_form_url(self):
        return reverse("test_result", kwargs={"pk": self.object.id})


def test_result(request, pk):
    if request.method != "POST":
        return redirect("user_test", pk=pk)

    test = get_object_or_404(Test, id=pk)
    questions = test.questions.all()
    answers = (request.POST.get(f"{q.id}_alternative") for q in questions)
    answered_alternatives = (
        q.alternatives.get(id=answer)
        for q, answer in zip(questions, answers)
        if answer is not None
    )
    weighted_res = chain.from_iterable(
        a.get_target_with_weights() for a in answered_alternatives
    )
    scores = Counter()
    for target, weight in weighted_res:
        scores[target] += weight
    if scores.most_common(1) == []:
        return redirect("user_test", pk=pk)
    ((result, _),) = scores.most_common(1)
    context = {
        "base_template": test.template,
        "title": result.title,
        "content": result.content,
    }
    return TemplateResponse(request, "interactive/user_test_result.html", context)

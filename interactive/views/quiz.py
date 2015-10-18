from django.views.generic import DetailView, ListView, DeleteView
from ..models.quiz import Quiz, QuizReply, QuestionReply, QuizScoreboard
from .mixins import ObjectOwnerMixin
from django.core.urlresolvers import reverse, reverse_lazy
from braces.views import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from braces.views import FormMessagesMixin


class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    paginate_by = 10
    template_name = "interactive/quiz_list.html"


class QuizView(LoginRequiredMixin, DetailView):
    """
    Shows all questions and answers.
    """

    model = Quiz
    template_name = "interactive/quiz.html"

    def get_form_url(self):
        return reverse('quiz_reply', kwargs={'pk': self.object.id})


def quiz_reply(request, pk):
    if request.user.is_authenticated():
        quiz = get_object_or_404(Quiz, id=pk)
        questions = quiz.questions.all()
        replies = []
        reply = QuizReply.objects.create(
            user=request.user,
            scoreboard_id=quiz.scoreboard.id,
            when=datetime.now()
        )

        for q in questions:
            answer = request.POST.get("{id}_alternative".format(id=q.id))
            if answer:
                replies.append(QuestionReply.objects.create(
                    question=q,
                    alternative=answer,
                    quiz_reply=reply
                ))
            else:
                messages.error(request, "Ugyldig")

        reply.save()
        return redirect(reply.get_absolute_url())
    else:
        messages.error(request, "Ikke logget inn.")
        return redirect('/')


class QuizResultView(LoginRequiredMixin, DetailView):
    model = QuizReply
    template_name = "interactive/quiz_result.html"
    context_object_name = "result"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = context['result'].scoreboard.quiz
        return context


class QuizScoreboardView(LoginRequiredMixin, DetailView):
    model = QuizScoreboard
    template_name = "interactive/scoreboard.html"
    context_object_name = "scoreboard"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = context['scoreboard'].replies.order_by('-score')
        return context


class QuizResultDeleteView(LoginRequiredMixin, ObjectOwnerMixin, FormMessagesMixin, DeleteView):
    model = QuizReply
    form_valid_message = "Svaret er slettet"
    form_invalid_message = "Svaret ble ikke slettet"

    def get_success_url(self):
        return reverse_lazy('quiz_score', kwargs={'pk': self.get_object().scoreboard.id})

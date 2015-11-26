from django.views.generic import DetailView, ListView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.views import login_required

from content.views.mixins import PublishedListMixin
from datetime import datetime
from braces.views import FormMessagesMixin, LoginRequiredMixin

from ..models.quiz import Quiz, QuizReply, QuizScoreboard, QuizReplyTimeout
from .mixins import ObjectOwnerMixin


class QuizListView(PublishedListMixin, LoginRequiredMixin, ListView):
    model = Quiz
    paginate_by = 10
    template_name = "interactive/quiz_list.html"


class QuizView(LoginRequiredMixin, DetailView):
    """
    Shows all questions and answers.
    """

    model = Quiz
    template_name = "interactive/quiz.html"

    def get_template_names(self):
        return self.template_name

    def get_form_url(self):
        return reverse('quiz_reply', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        QuizReply.objects.create(
            user=self.request.user,
            scoreboard_id=self.object.scoreboard.id,
            start=datetime.now(),
            when=datetime.now()
        )
        return context


@login_required
def quiz_reply(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)
    questions = quiz.questions.all()
    reply = QuizReply.objects.filter(
        user=request.user,
        scoreboard_id=quiz.scoreboard.id
    ).order_by('-when')[0]

    format_string = "{}_alternative"
    answers = (request.POST.get(format_string.format(q.id)) for q in questions)

    q_and_a = [
        (q, int(answer))
        for q, answer in zip(questions, answers)
        if answer is not None
    ]
    try:
        reply.add_question_replies(q_and_a)
    except QuizReplyTimeout:
        messages.info(request, "Beklager, tiden gikk ut")
        return redirect('/')

    messages.info(request, "Du svarte på {} av {} spørsmål.".format(len(q_and_a), len(questions)))
    return redirect(reply.get_absolute_url())


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

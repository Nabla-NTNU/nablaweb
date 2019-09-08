from django.views.generic import DetailView, ListView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.views import login_required
from django.http import Http404

from datetime import datetime
from uuid import uuid4
from braces.views import FormMessagesMixin, LoginRequiredMixin

from ..models.quiz import Quiz, QuizReply, QuizScoreboard, QuizReplyTimeout
from .mixins import ObjectOwnerMixin


# Key in the user' session used to store start-times for quizes
QUIZREPLIES_SESSIONKEY = "quizreplies_timestamps"
# Date format used to store datetimes in the users' session
DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


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

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=None)
        if obj.published or self.request.user.has_perm("interactive.change_quiz"):
            return obj
        else:
            raise Http404("Ikke publisert")

    def get_template_names(self):
        return self.template_name

    def get_form_url(self):
        return reverse('quiz_reply', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Generate a unique id for the quizreply and store it on the view
        # This is later sent with the user's POST request as a hidden value
        self.quiz_reply_id = uuid4().hex

        # Create the dict for id, start-time pairs if it does not exist yet
        if QUIZREPLIES_SESSIONKEY not in self.request.session:
            self.request.session[QUIZREPLIES_SESSIONKEY] = {}

        # Store the quizreply id in the users session along with
        # its corresponding start-time
        # The time is converted to a string because a datetime object isn't
        # JSON-serializable, and can't be stored in the session
        self.request.session[QUIZREPLIES_SESSIONKEY][self.quiz_reply_id] = \
            datetime.strftime(datetime.now(), DATE_FORMAT)

        # Mark the session as modified, because we are modifying a nested object
        self.request.session.modified = True

        return context


@login_required
def quiz_reply(request, pk):
    if QUIZREPLIES_SESSIONKEY not in request.session:
        # This entry in the session is created when the user starts the quiz.
        # Could be missing if the users session is invalidated while they are
        # taking the quiz, or there is foul play.
        messages.info(request, "Beklager, det har oppstått en feil. (Brukte du for lang tid?)")
        return redirect('/quiz')

    quiz_reply_id = request.POST.get("quiz_reply_id")

    if quiz_reply_id not in request.session[QUIZREPLIES_SESSIONKEY]:
        # The quiz reply id submitted with the POST request is invalid.
        # Most likely foul play.
        messages.info(request, "Beklager, det har oppstått en feil.")
        return redirect('/quiz')

    # Get the start-time of the submitted quizreply
    starttimestring = request.session[QUIZREPLIES_SESSIONKEY][quiz_reply_id]
    # Converted to a datetime
    startdatetime = datetime.strptime(starttimestring, DATE_FORMAT)

    # Remove the id and mark the session as modified
    del request.session[QUIZREPLIES_SESSIONKEY][quiz_reply_id]
    request.session.modified = True

    quiz = get_object_or_404(Quiz, id=pk)
    questions = quiz.questions.all()

    answers = (request.POST.get(f"{q.id}_alternative") for q in questions)

    q_and_a = [
        (q, int(answer))
        for q, answer in zip(questions, answers)
        if answer is not None
    ]

    if len(q_and_a) == 0:
        # User didn't answer any questions -> deny the reply
        messages.info(request, "Du må svare på minst ett spørsmål!")
        return redirect('/quiz')

    # Create the reply
    reply = QuizReply.objects.create(
        user=request.user,
        scoreboard=quiz.scoreboard,
        start=startdatetime,
        when=startdatetime
    )

    try:
        reply.add_question_replies(q_and_a)
    except QuizReplyTimeout:
        messages.info(request, "Beklager, tiden gikk ut")
        return redirect('/')
    else:
        reply.save()

    messages.info(request, f"Du svarte på {len(q_and_a)} av {len(questions)} spørsmål.")
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

"""
Views for poll app
"""
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView

from braces.views import FormMessagesMixin, LoginRequiredMixin

from .forms import ChoiceFormSet, PollForm
from .models import Choice, Poll, UserHasVoted


@login_required
def vote(request, poll_id):
    """
    View for registering a vote for the logged in user.
    """
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        choice = poll.choices.get(pk=request.POST["choice"])
        choice.vote(request.user)
    except (KeyError, Choice.DoesNotExist):
        messages.warning(request, "Du valgte ikke et svaralternativ")
    except UserHasVoted:
        messages.error(request, "Du har allerede stemt i denne avstemningen!")
    else:
        messages.success(request, f'Du har svart på "{poll.question}"')

    redirect_to = request.POST.get("next", request.META.get("HTTP_REFERER", "/"))
    return redirect(redirect_to)


class PollListView(LoginRequiredMixin, ListView):
    """
    Shows polls
    """

    model = Poll
    paginate_by = 10
    template_name = "poll/poll_list.html"
    queryset = Poll.objects.order_by("-creation_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["next"] = (
            self.request.path + "?page=" + self.request.GET.get("page", "1")
        )

        for poll in context["poll_list"]:
            poll.voted = poll.user_has_voted(user)
        return context


class UserPollsView(LoginRequiredMixin, ListView):
    """
    The current users polls and a form for creating a new.
    """

    model = Poll
    paginate_by = 10
    template_name = "poll/user_polls.html"

    def get_queryset(self):
        return Poll.objects.order_by("-creation_date").filter(
            is_user_poll=True, created_by=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        for poll in context["poll_list"]:
            poll.voted = poll.user_has_voted(user)
        return context


class UserPollCRUDMixin(LoginRequiredMixin, FormMessagesMixin):
    """
    View mixin to set the common attributes and methods of
    Create-, Update- and DeleteViews for user polls.

    The commonality is most evident in Create and UpdateView,
    and the DeleteView doesn't actually use any of the form processing.
    """

    model = Poll
    form_invalid_message = "Ikke riktig utfylt."
    form_class = PollForm

    def get_success_url(self):
        """The url to redirect to after successfully creating, updating or deleting."""
        return reverse("poll_user")


class CreatorRequiredMixin:
    """
    View mixin for making sure only the creator can use the view.
    """

    def dispatch(self, request, *args, **kwargs):
        """Extends dispatch method in views"""
        if self.get_object().created_by != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class CreateUserPollView(UserPollCRUDMixin, CreateView):  # pylint: disable=R0901
    """
    View allowing users to create a poll.
    """

    form_valid_message = "Avstemning publisert."
    template_name = "poll/poll_create.html"

    def get(self, request, *args, **kwargs):
        """Handles GET requests and instantiates blank versions of the form and its inline formsets."""
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        choice_form = ChoiceFormSet()
        return self.render_to_response(
            self.get_context_data(
                form=form,
                choice_form=choice_form,
            )
        )

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for validity.
        """
        self.object = None
        self.user = request.user
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        choice_form = ChoiceFormSet(self.request.POST)
        if form.is_valid() and choice_form.is_valid():
            return self.form_valid(form, choice_form)
        else:
            return self.form_invalid(form, assignment_question_form)  # noqa: F821

    def form_valid(self, form, choice_form):
        """
        Called if all forms are valid, Creates Poll instance along with the associated Choice
        instances, then redirects to success url.

        Args:
            form: Poll Form
            choice_form: Choice Form

        Returns: an HttpResponse to success url
        """
        # Save poll object from form and assign it to self.object
        self.object = form.save(commit=False)
        # Pre-processing for Poll instance here ...
        self.object.publication_date = datetime.now()
        self.object.is_user_poll = True
        self.object.is_current = False
        if not self.object.created_by and self.user is not None:
            self.object.created_by = self.user
        self.object.save()

        # Saving Choice instances
        choices = choice_form.save(commit=False)
        for ch in choices:
            ch.poll = self.object
            ch.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, choice_form):
        """
        Called if a form is invalid. Re-renders the context data with the data-filled
        forms and errors.

        Args:
            form: Poll Form
            choice_form: Choice Form
        """
        return self.render_to_response(
            self.get_context_data(form=form, choice_form=choice_form)
        )


class DeleteUserPollView(UserPollCRUDMixin, CreatorRequiredMixin, DeleteView):
    """
    View allowing users to delete their created polls.
    """

    form_invalid_message = "Noe gikk galt i slettingen."

    def get_form_valid_message(self):
        return f"Du har slettet {self.object.question}"

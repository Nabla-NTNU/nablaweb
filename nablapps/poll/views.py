"""
Views for poll app
"""
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin, FormMessagesMixin

from .forms import PollForm
from .models import Poll, Choice, UserHasVoted


@login_required
def vote(request, poll_id):
    """
    View for registering a vote for the logged in user.
    """
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        choice = poll.choices.get(pk=request.POST['choice'])
        choice.vote(request.user)
    except (KeyError, Choice.DoesNotExist):
        messages.warning(request, 'Du valgte ikke et svaralternativ')
    except UserHasVoted:
        messages.error(request, 'Du har allerede stemt i denne avstemningen!')
    else:
        messages.success(request, f'Du har svart på "{poll.question}"')

    redirect_to = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(redirect_to)


class PollListView(LoginRequiredMixin, ListView):
    """
    Shows polls
    """
    model = Poll
    paginate_by = 10
    template_name = "poll/poll_list.html"
    queryset = Poll.objects.order_by('-creation_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        for poll in context['poll_list']:
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
        return Poll.objects.order_by('-creation_date').filter(is_user_poll=True,
                                                              created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PollForm()
        user = self.request.user
        for poll in context['poll_list']:
            poll.voted = poll.user_has_voted(user)
        return context


class UserPollCRUDMixin(LoginRequiredMixin, FormMessagesMixin):
    """
    View mixin to set the common attributes and methods of
    Create-, Update- and DeleteViews for user polls.

    The commonality is most evident in Create and UpdateView,
    and the DeleteView doesn't actually use any of the form processing.
    """
    form_class = PollForm
    model = Poll
    form_invalid_message = "Ikke riktig utfylt."
    template_name = 'form.html'

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.

        Extends method from ModelFormMixin in django.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        """The url to redirect to after successfully creating, updating or deleting."""
        return reverse('poll_user')


class CreatorRequiredMixin:
    """
    View mixin for making sure only the creator can use the view.
    """
    def dispatch(self, request, *args, **kwargs):
        """Extends dispatch method in views"""
        if self.get_object().created_by != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class CreateUserPollView(UserPollCRUDMixin, CreateView): # pylint: disable=R0901
    """
    View allowing users to create a poll.
    """
    form_valid_message = "Avstemning publisert."


class UpdateUserPollView(UserPollCRUDMixin, CreatorRequiredMixin, UpdateView): # pylint: disable=R0901
    """
    View allowing users to edit their created polls.
    """
    form_valid_message = "Avstemning oppdatert."


class DeleteUserPollView(UserPollCRUDMixin, CreatorRequiredMixin, DeleteView):
    """
    View allowing users to delete their created polls.
    """
    form_invalid_message = "Noe gikk galt i slettingen."

    def get_form_valid_message(self):
        return f"Du har slettet {self.object.question}"

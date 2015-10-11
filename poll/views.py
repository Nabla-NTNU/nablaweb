# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from braces.views import LoginRequiredMixin, FormMessagesMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Poll, Choice, UserHasVoted
from .forms import PollForm


@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        choice = poll.choices.get(pk=request.POST['choice'])
        choice.vote(request.user)
    except (KeyError, Choice.DoesNotExist):
        messages.warning(request, 'Du valgte ikke et svaralternativ')
    except UserHasVoted:
        messages.error(request, 'Du har allerede stemt i denne avstemningen!')
    else:
        messages.success(request, u'Du har svart på "%s"' % poll.question)

    redirect_to = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(redirect_to)


class PollListView(LoginRequiredMixin, ListView):
    """
    Shows user defined polls
    """
    model = Poll
    paginate_by = 10
    template_name = "poll/poll_list.html"
    queryset = Poll.objects.order_by('-creation_date').filter(is_user_poll=True)

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
    form_class = PollForm
    model = Poll
    form_invalid_message = "Ikke riktig utfylt."
    template_name = 'form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.view = self
        return form

    def get_success_url(self):
        return reverse('poll_user')


class CreatorRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().created_by != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class CreateUserPollView(UserPollCRUDMixin, CreateView):
    form_valid_message = "Avstemning publisert."


class UpdateUserPollView(UserPollCRUDMixin, CreatorRequiredMixin, UpdateView):
    form_valid_message = "Avstemning oppdatert."


class DeleteUserPollView(UserPollCRUDMixin, CreatorRequiredMixin, DeleteView):
    form_invalid_message = "Noe gikk galt i slettingen."

    def get_form_valid_message(self):
        return "Du har slettet {}".format(self.object.question)

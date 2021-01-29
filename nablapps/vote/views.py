from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .models import Voting, Alternative, UserAlreadyVoted, VotingDeactive
from .forms import AlternativeFormset

####################
### Admin views ####
####################
# Remeber to make permission requirement


class VotingList(ListView):
    """List of all votings"""
    model = Voting
    template_name = "vote/voting_list.html"


class CreateVoting(CreateView):
    """View for creating new votings"""
    template_name = "vote/voting_form.html"
    model = Voting
    fields = ["title", "description"]
    success_url = reverse_lazy('voting-list')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['alternatives'] = AlternativeFormset(self.request.POST)
        else:
            context['alternatives'] = AlternativeFormset()
        return context


    def form_valid(self, form):
        """Called if all forms are valid. Creates voting and associated alternatives"""
        context = self.get_context_data()
        alternatives = context["alternatives"]
        with transaction.atomic():
            self.object = form.save()
            if alternatives.is_valid():
                alternatives.instance = self.object
                alternatives.save()
        return super().form_valid(form)


class VotingDetail(DetailView):
    model = Voting
    template_name = "vote/voting_detail.html"


def activate_voting(request, pk):
    voting = Voting.objects.get(pk=pk)
    voting.is_active = True
    voting.save()
    return redirect("voting-detail", pk=pk)


def deactivate_voting(request, pk):
    voting = Voting.objects.get(pk=pk)
    voting.is_active = False
    voting.save()
    return redirect("voting-detail", pk=pk)


###########################################
### Non admin vies, only login required ###
###########################################


class Vote(LoginRequiredMixin, DetailView):
    model = Voting
    template_name = "vote/voting_vote.html"


@login_required
def submit_vote(request, pk):
    voting = get_object_or_404(Voting, pk=pk)
    try:
        alternative = voting.alternatives.get(pk=request.POST["alternative"])
        alternative.add_vote(request.user)
    except (KeyError, Alternative.DoesNotExist):
        messages.warning(request, "Du har ikke valgt et alternativ.")
        return redirect("voting-vote", pk=pk)
    except UserAlreadyVoted:
        messages.error(request, "Du har allerede stemt i denne avstemningen!")
    except VotingDeactive:
        messages.error(request, "Denne avstemningen er ikke lenger åpen for stemming!")
    else:
        messages.success(request, f"Suksess! Du har stemt i avstemningen {voting.title}")
    return redirect("active-voting-list")


class ActiveVotingList(ListView):
    model = Voting
    template_name = "vote/active_voting_list.html"
    

    def get_queryset(self):
        return self.model.objects.exclude(is_active=False)


def main_redirect(request):
    pass


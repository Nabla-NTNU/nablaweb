from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .models import Votation, Alternative, UserAlreadyVoted, VotationDeactive
from .forms import AlternativeFormset

####################
### Admin views ####
####################
# Remeber to make permission requirement


class VotationList(ListView):
    """List of all votations"""
    model = Votation
    template_name = "vote/votation_list.html"


class CreateVotation(CreateView):
    """View for creating new votations"""
    template_name = "vote/votation_form.html"
    model = Votation
    fields = ["title", "description"]
    success_url = reverse_lazy('votation-list')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['alternatives'] = AlternativeFormset(self.request.POST)
        else:
            context['alternatives'] = AlternativeFormset()
        return context


    def form_valid(self, form):
        """Called if all forms are valid. Creates votation and associated alternatives"""
        context = self.get_context_data()
        alternatives = context["alternatives"]
        with transaction.atomic():
            self.object = form.save()
            if alternatives.is_valid():
                alternatives.instance = self.object
                alternatives.save()
        return super().form_valid(form)


class VotationDetail(DetailView):
    model = Votation
    template_name = "vote/votation_detail.html"


def activate_votation(request, pk):
    votation = Votation.objects.get(pk=pk)
    votation.is_active = True
    votation.save()
    return redirect("votation-detail", pk=pk)


def deactivate_votation(request, pk):
    votation = Votation.objects.get(pk=pk)
    votation.is_active = False
    votation.save()
    return redirect("votation-detail", pk=pk)


###########################################
### Non admin vies, only login required ###
###########################################


class Vote(LoginRequiredMixin, DetailView):
    model = Votation
    template_name = "vote/votation_vote.html"


@login_required
def submit_vote(request, pk):
    votation = get_object_or_404(Votation, pk=pk)
    try:
        alternative = votation.alternatives.get(pk=request.POST["alternative"])
        alternative.add_vote(request.user)
    except (KeyError, Alternative.DoesNotExist):
        messages.warning(request, "Du har ikke valgt et alternativ.")
        return redirect("votation-vote", pk=pk)
    except UserAlreadyVoted:
        messages.error(request, "Du har allerede stemt i denne avstemningen!")
    except VotationDeactive:
        messages.error(request, "Denne avstemningen er ikke lenger åpen for stemming!")
    else:
        messages.success(request, f"Suksess! Du har stemt i avstemningen {votation.title}")
    return redirect("active-votation-list")


class ActiveVotationList(ListView):
    model = Votation
    template_name = "vote/active_votation_list.html"
    

    def get_queryset(self):
        return self.model.objects.exclude(is_active=False)


def main_redirect(request):
    pass


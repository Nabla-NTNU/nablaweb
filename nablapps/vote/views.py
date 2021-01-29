from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Votation
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


class Vote(LoginRequiredMixin, DetailView):
    model = Votation
    template_name = "vote/votation_vote.html"



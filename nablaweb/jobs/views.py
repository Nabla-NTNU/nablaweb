# -*- coding: utf-8 -*-

from django.views.generic import ListView, DetailView
from content.templatetags.listutil import row_split
from jobs.models import Advert, Company, YearChoices, RelevantForChoices, TagChoices
from django.shortcuts import get_object_or_404
from datetime import datetime


def active_jobs(request):
    """Used as a template context processor."""
    active_jobs = Advert.objects.all()
    return {'active_jobs': active_jobs}


def split_into_rows(jobs):
    """Deler f.eks. opp [1, 2, 3, 4, 5] til [[1, 2], [3, 4], [5]]."""
    return row_split(jobs, 2) if jobs else None


class GenericJobsList(ListView):
    """Abstrakt rotklasse som håndterer info for sidebaren."""
    context_object_name = 'jobs_list'
    template_name = 'jobs/jobs_list.html'
    paginate_by = 8
	
    def get_context_data(self, **kwargs):
        context = super(GenericJobsList, self).get_context_data(**kwargs)

        context['years'] = YearChoices.objects.all()
        context['choices'] = RelevantForChoices.objects.all()
        context['tags'] = TagChoices.objects.all() 
        context['jobs_rows'] = split_into_rows(self.object_list)

        return context


class EverythingList(GenericJobsList):
    """Alle aktive stillingsannonser."""
    def get_queryset(self):
        return Advert.objects.all().order_by('-created_date', 'headline').exclude(removal_date__lte=datetime.now())


class CompanyList(GenericJobsList):
    """Stillingsannonser for en spesifikk bedrift."""
    def get_queryset(self):
        company = get_object_or_404(Company, name__iexact=self.kwargs['slug'])
        return Advert.objects.filter(company=company).order_by('-created_date', 'headline')


class YearList(GenericJobsList):
    """Stillingsannonser som er lagt inn dette året."""
    def get_queryset(self):
        return Advert.objects.filter(created_date__year=self.kwargs['year'])


class MonthList(GenericJobsList):
    """Stillingsannonser som er lagt inn denne måneden."""
    def get_queryset(self):
        return Advert.objects.filter(created_date__year=self.kwargs['year']).filter(created_date__month=self.kwargs['month'])


class TagList(GenericJobsList):
    """Stillingsannonser merket med en spesifikk tag."""
    def get_queryset(self):
        return Advert.objects.filter(tags__tag__iexact=self.kwargs['tag']).order_by('-created_date', 'headline').exclude(removal_date__lte=datetime.now())


class RelevantForLinjeList(GenericJobsList):
    """Stillingsannonser merket som relevante for en spesifikk studieretning."""
    def get_queryset(self):
        return Advert.objects.filter(relevant_for_group__studieretning__iexact=self.kwargs['linje']).order_by('-created_date', 'headline').exclude(removal_date__lte=datetime.now())


class RelevantForYearList(GenericJobsList):
    """Stillingsannonser merket som relevante for et spesifikt årskull."""
    def get_queryset(self):
        return Advert.objects.filter(relevant_for_year__year__iexact=self.kwargs['year']).order_by('-created_date', 'headline').exclude(removal_date__lte=datetime.now())


class ShowJob(DetailView):
    """Detaljviewet for en spesifikk stillingsannonse."""
    model = Advert
    context_object_name = 'job'
    template_name = "jobs/jobs_detail.html"

# -*- coding: utf-8 -*-

# Views for stillingsannonser-appen

from django.views.generic import ListView, DetailView
from nablaweb.news.views import *
from nablaweb.jobs.models import Advert, Company, YearChoices, RelevantForChoices, TagChoices
from django.shortcuts import get_object_or_404
from datetime import datetime

class GenericJobsList(ListView):
    model = Advert
    context_object_name = 'jobs_list'
    template_name = 'jobs/jobs_list.html'
    paginate_by = 8
	
    def get_context_data(self, **kwargs):
        context = super(GenericJobsList, self).get_context_data(**kwargs)

        #jobs_list = context['jobs_list']
        jobs = Advert.objects.all().order_by('-created_date', 'headline').exclude(removal_date__lte=datetime.now())

        if jobs:
            context['jobs_list'] = jobs
        else:
            context['jobs_list'] = None

        years = YearChoices.objects.all()
        choices = RelevantForChoices.objects.all()
        tags = TagChoices.objects.all() 

        if years:
            context['years'] = years
        else:
            context['years'] = None

        if choices:
            context['choices'] = choices
        else:
            context['choices'] = None

        if tags:
            context['tags'] = tags
        else:
            context['tags'] = None

        if jobs:
            # Deler f.eks. opp [1, 2, 3, 4, 5] til [[1, 2], [3, 4], [5]]
            context['jobs_rows'] = listutil.row_split(jobs[0:], 2)

        return context

class EverythingList(GenericJobsList):
    @staticmethod
    def active_jobs(request):
        active_jobs = Advert.objects.filter()
        return {'active_jobs': active_jobs}

    def get_queryset(self):
        return Advert.objects.filter()

activej = EverythingList.active_jobs

class CompanyList(GenericJobsList):
    def get_queryset(self):
        company = get_object_or_404(Company, name__iexact=self.kwargs['slug'])
        return Advert.objects.filter(company=company)


class YearList(GenericJobsList):  # Stillingsannonser som er lagt inn dette året
    def get_queryset(self):
        return Advert.objects.filter(created_date__year=self.kwargs['year'])

class TagList(GenericJobsList):
    def get_queryset(self):
        return Advert.objects.filter(tags__tag__iexact=self.kwargs['tag']).distinct()

class MonthList(GenericJobsList):  # Stillingsannonser som er lagt inn denne måneden
    def get_queryset(self):
        return Advert.objects.filter(created_date__year=self.kwargs['year']).filter(created_date__month=self.kwargs['month'])


class RelevantForLinjeList(GenericJobsList):
    def get_queryset(self):
        return Advert.objects.filter(relevant_for_group__studieretning__iexact=self.kwargs['linje']).distinct()


class RelevantForYearList(GenericJobsList):
    def get_queryset(self):
        return Advert.objects.filter(relevant_for_year__year__iexact=self.kwargs['year']).distinct()


class ShowJob(DetailView):
    model = Advert
    context_object_name = 'job'
    template_name = "jobs/jobs_detail.html"

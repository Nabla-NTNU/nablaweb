# -*- coding: utf-8 -*-

# Views for stillingsannonser-appen

from django.views.generic import ListView, DetailView
from nablaweb.news.views import *
from nablaweb.jobs.models import Advert, Company
from django.shortcuts import get_object_or_404


class GenericJobsList(ListView):
    model = Advert
    context_object_name = 'jobs_list'
    template_name = 'jobs/jobs_list.html'
    paginate_by = 10


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
        company = get_object_or_404(Company, name__iexact=self.kwargs['company'])
        return Advert.objects.filter(company=company)


class YearList(GenericJobsList):  # Stillingsannonser som er lagt inn dette året
    def get_queryset(self):
        return Advert.objects.filter(created_date__year=self.kwargs['year'])


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

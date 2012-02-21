# -*- coding: utf-8 -*-

# Views for stillingsannonser-appen

from django.views.generic import ListView, RedirectView, DetailView
from nablaweb.news.views import *
from nablaweb.jobs.models import *
from django.shortcuts import get_object_or_404, get_list_or_404

class GenericList(ListView):
    context_object_name = "content_list"
    template_name = "content/content_list.html"
    
class EverythingList(ListView):
    model = Advert
    context_object_name = 'jobs_list'
    template_name = 'jobs/jobs_list.html'

    paginate_by = 10
    
    @staticmethod
    def active_jobs(request):
        active_jobs = Advert.objects.filter()
        return {'active_jobs': active_jobs}

    def get_queryset(self):
        return Advert.objects.filter()

activej = EverythingList.active_jobs

class CompanyList(GenericList):
    def get_queryset(self):  
        company = get_object_or_404(Company, headline__iexact=self.kwargs['company'])
        return Advert.objects.filter(company=company)

class DateList(GenericList):
    pass
    
class ShowJob(DetailView):
    model = Advert
    context_object_name = 'jobs_detail'
    template_name = "jobs/jobs_detail.html"

class RedirectJob(RedirectView):
    def get_redirect_url(self, **kwargs):
        pid = get_object_or_404(Advert, pk=self.kwargs['pk'])
        url = '/stillinger/' + pid.company.headline + '/' + str(pid.pk)
        return url

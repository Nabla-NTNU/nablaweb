# -*- coding: utf-8 -*-

# Views for stillingsannonser-appen

from nablaweb.content.views import *
from nablaweb.jobs.models import Advert, Company
from django.shortcuts import get_object_or_404

class GenericList(ListView):
    context_object_name = "content_list"
    template_name = "content/content_list.html"
    
class EverythingList(GenericList):
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
    pass

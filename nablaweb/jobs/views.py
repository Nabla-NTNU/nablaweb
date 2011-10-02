# -*- coding: utf-8 -*-

# Views for stillingsannonser-appen

from nablaweb.content.views import *
from nablaweb.jobs.models import Advert, Company

class List(ListView):
    context_object_name = "content_list"
    template_name = "content/content_list.html"
    
    def get_queryset(self):
        company = get_object_or_404(Company, name__iexact=self.args[0])
        return Advert.objects.filter(company=company)

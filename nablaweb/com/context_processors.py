# -*- coding: utf-8 -*-

from com.models import ComPage

def com_context(request):
    coms = ComPage.objects.all().order_by('com__name')
    return {'coms': coms}

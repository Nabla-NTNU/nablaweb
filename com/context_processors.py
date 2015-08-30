# -*- coding: utf-8 -*-

from com.models import ComPage


def com_context(request):
    return {'coms': ComPage.objects.order_by('com__name')}

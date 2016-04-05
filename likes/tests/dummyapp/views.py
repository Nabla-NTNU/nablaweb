from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.template.loader import get_template
from django.views.generic import ListView, View

from .models import DummyModel
from likes.models import user_likes, get_like_count


class DummyList(ListView):
    model = DummyModel
#    def get(self, request, *args, **kwargs):
#        dummies = DummyModel.objects.all()
#        context_data = {'object_list': dummies}
#        context = RequestContext(request, context_data)
#        template = get_template('dummyapp/dummymodel_list.html')
#        other_template = template.template
#        string = other_template.render(context)
#        print("dummylist: {}".format(id(context)))
##        return HttpResponse(string)

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from feedback.forms import FeedbackModelForm
from feedback.models import Feedback
from nablaweb.homepage.views import start as index

def feedback_form(request):
    if request.method == 'POST':
        form = FeedbackModelForm(request.POST)
        # print request.META.get("REMOTE_ADDR")
        if form.is_valid():
            print form.cleaned_data.get("created_by")
            if request.user.is_authenticated(): created_by = unicode(request.user)
            else: created_by = form.cleaned_data.get("created_by")
            
            feedback = Feedback(headline=form.cleaned_data.get("headline"), created_by=created_by, body=form.cleaned_data.get("body"))
            feedback.save()
            
            return render_to_response('feedback/feedback_success.html', {'post':feedback}, context_instance=RequestContext(request))
    else:
        form = FeedbackModelForm()
            
    return render_to_response('feedback/feedback_form.html', {'form':form,}, context_instance=RequestContext(request))
    


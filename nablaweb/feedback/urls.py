from django.conf.urls.defaults import *
from nablaweb.feedback.forms import FeedbackModelForm

urlpatterns = patterns('nablaweb.feedback.views',

    (r'^$', 'feedback_form'),
)

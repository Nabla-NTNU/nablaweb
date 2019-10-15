from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


def index(request):
    return HttpResponse("Index yo")


# View for displaying Channels
class IndexView(TemplateView):
    template_name = "nablaforum/forum_index.html"
    pass


# View for displaying Threads in a channel
class ChannelIndexView(TemplateView):
    pass


# View for displaying messages in a thread
class ThreadView(TemplateView):
    pass

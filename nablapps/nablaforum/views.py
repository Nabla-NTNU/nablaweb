from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView

from .models import Channel, Thread, Message

def index(request):
    return HttpResponse("Index yo")


# View for displaying Channels
class IndexView(ListView):
    model = Channel
    #paginate_by = 10
    template_name = "nablaforum/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #channel_ids = [obj.pk for obj in self.model.objects.all()]
        #context['channel_ids'] = channel_ids
        return context


# View for displaying Threads in a channel
class ChannelIndexView(TemplateView):
    model = Thread
    template_name = "nablaforum/channel.html"

    def get_context_data(self, channel_id, **kwargs):
        context = super().get_context_data(**kwargs)
        query_set = self.model.objects.filter(channel__id=channel_id)
        context['threads'] = query_set
        context['channel_id'] = channel_id
        return context


# View for displaying messages in a thread
class ThreadView(TemplateView):
    model = Message
    template_name = "nablaforum/thread.html"

    def get_context_data(self, channel_id, thread_id, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = self.model.objects.filter(thread__id=thread_id)
        thread = Thread.objects.get(pk=thread_id)
        context['messages'] = messages
        context['thread'] = thread
        return context

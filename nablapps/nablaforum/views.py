from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, FormView

from .models import Channel, Thread, Message
from .forms import ThreadForm, MessageForm

def index(request):
    return HttpResponse("Index yo")


# View for displaying Channels
class IndexView(ListView):
    model = Channel
    #paginate_by = 10
    template_name = "nablaforum/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# View for displaying Threads in a channel
class ChannelIndexView(FormView):
    model = Thread
    template_name = "nablaforum/channel.html"
    form_class = ThreadForm


    def form_valid(self, form):
        form_data = form.cleaned_data
        channel_id = self.kwargs['channel_id']
        channel = Channel.objects.get(pk=channel_id)
        new_thread = self.model.objects.create(
                                        channel = channel,
                                        threadstarter = self.request.user,
                                        title = form_data['title_field'],
                                        text = form_data['text_field'],)
        return self.render_to_response(self.get_context_data(form=form))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        channel_id = self.kwargs['channel_id']
        channel = Channel.objects.get(pk=channel_id)
        query_set = self.model.objects.filter(channel__id=channel_id)

        context['threads'] = query_set
        context['channel_id'] = channel_id
        context['channel'] = channel
        return context


# View for displaying messages in a thread
class ThreadView(FormView):
    model = Message
    template_name = "nablaforum/thread.html"
    form_class = MessageForm

    
    def form_valid(self, form):
        form_data = form.get_data()
        thread_id = self.kwargs['thread_id']
        thread = Thread.objects.get(pk=thread_id)
        new_message = self.model.objects.create(
                                        thread = thread,
                                        user = self.request.user,
                                        message = form_data['message_field'],)
        return self.render_to_response(self.get_context_data(form=form))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        channel_id = self.kwargs['channel_id']
        thread_id = self.kwargs['thread_id']
        messages = self.model.objects.filter(thread__id=thread_id)
        thread = Thread.objects.get(pk=thread_id)
        context['thread_messages'] = messages
        context['thread'] = thread
        context['channel_id'] = channel_id
        print(context)
        return context

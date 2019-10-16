from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, FormView

from .models import Channel, Thread, Message
from .forms import ThreadForm, MessageForm, ChannelForm
from nablapps.accounts.models import NablaGroup

# View for displaying Channels
class IndexView(LoginRequiredMixin, FormView):
    model = Channel
    template_name = "nablaforum/index.html"
    form_class = ChannelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['groups'] = NablaGroup.objects.filter(pk__in=self.request.user.groups.all().values_list('pk'))
        return kwargs
    
    def form_valid(self, form):
        form_data = form.cleaned_data
        try:
            new_channel = self.model.objects.create(
                                            group = form_data['group'],
                                            name = form_data['name'],
                                            description = form_data['description'],)
        except:
            print('Ops! Kunne ikke opprette kanal, ugyldig verdi i feltene!')
        return self.render_to_response(self.get_context_data(form=form))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        channels = Channel.objects.filter(group__in=user.groups.all())
        context['channels'] = channels
        return context


# View for displaying Threads in a channel
class ChannelIndexView(LoginRequiredMixin, FormView):
    model = Thread
    template_name = "nablaforum/channel.html"
    form_class = ThreadForm


    def form_valid(self, form):
        form_data = form.cleaned_data
        channel_id = self.kwargs['channel_id']
        channel = Channel.objects.get(pk=channel_id)
        try:
            new_thread = self.model.objects.create(
                                            channel = channel,
                                            threadstarter = self.request.user,
                                            title = form_data['title_field'],
                                            text = form_data['text_field'],)
        except:
            print('Ops! Kunne ikke opprette tråd, ugyldig verdi i feltene!')
        return self.render_to_response(self.get_context_data(form=form))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        channel_id = self.kwargs['channel_id']
        channel = get_object_or_404(Channel, pk=channel_id)
        query_set = self.model.objects.filter(channel__id=channel_id)

        context['threads'] = query_set
        context['channel_id'] = channel_id
        context['channel'] = channel
        return context


# View for displaying messages in a thread
class ThreadView(LoginRequiredMixin, FormView):
    model = Message
    template_name = "nablaforum/thread.html"
    form_class = MessageForm

    
    def form_valid(self, form):
        form_data = form.cleaned_data
        thread_id = self.kwargs['thread_id']
        thread = get_object_or_404(Thread, pk=thread_id)
        try:
            new_message = self.model.objects.create(
                                            thread = thread,
                                            user = self.request.user,
                                            message = form_data['message_field'],)
        except:
            print('Ops! Kunne ikke opprette kanal, ugyldig verdi i feltene!')
        return self.render_to_response(self.get_context_data(form=form))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        channel_id = self.kwargs['channel_id']
        thread_id = self.kwargs['thread_id']
        messages = self.model.objects.filter(thread__id=thread_id)
        thread = get_object_or_404(Thread, pk=thread_id)
        context['thread_messages'] = messages
        context['thread'] = thread
        context['channel_id'] = channel_id
        print(context)
        return context

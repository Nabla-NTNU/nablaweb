from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, FormView
from django.core.paginator import Paginator

from .models import Channel, Thread, Message
from .forms import ThreadForm, MessageForm, ChannelForm, JoinChannelsForm
from nablapps.accounts.models import NablaGroup


class MainView(TemplateView):
    template_name = "nablaforum/forum.html"
    paginate_thread_by = 5


    def post(self, request, **kwargs):
        thread_form = ThreadForm(self.request.POST)
        message_form = MessageForm(self.request.POST)

        if thread_form.is_valid():
            form_data = thread_form.cleaned_data
            channel_id = self.kwargs['channel_id']
            channel = Channel.objects.get(pk=channel_id)
            print('HEHEHE: \n', form_data, channel_id)
            print(channel)
            try:
                new_thread = Thread.objects.create(
                                                channel = channel,
                                                threadstarter = self.request.user,
                                                title = form_data['title_field'],
                                                text = form_data['text_field'],)
            except:
                print('Ops! Kunne ikke opprette tråd, ugyldig verdi i feltene!')
            return redirect('forum-main', channel_id=channel_id, thread_id=0)

        elif message_form.is_valid():
            form_data = message_form.cleaned_data
            thread_id = self.kwargs['thread_id']
            channel_id = self.kwargs['channel_id']
            thread = get_object_or_404(Thread, pk=thread_id)
            try:
                new_message = Message.objects.create(
                                                thread = thread,
                                                user = self.request.user,
                                                message = form_data['message_field'],)
                new_message.read_by_user.add(self.request.user)
            except:
                print('Ops! Kunne ikke opprette kanal, ugyldig verdi i feltene!')
            return redirect('forum-main', channel_id=channel_id, thread_id=thread_id)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # All channels belonging to users group
        group_channels = Channel.objects.filter(group__in=user.groups.all()).order_by('-pk')

        # Ordinary channels the user is member of
        common_channels = Channel.objects.filter(group=None).filter(members=self.request.user)

        # Pinned channels
        #pinned_channels = Channel.filter(is_pinned=True)

        # Feeds
        feeds = Channel.objects.filter(is_feed=True)

        # get chosen channel and belonging threads
        chosen_channel_id = self.kwargs['channel_id']
        chosen_channel = Channel.objects.get(pk=chosen_channel_id)
        channel_threads = Thread.objects.filter(channel__id=chosen_channel_id).order_by('-pk')
        paginator = Paginator(channel_threads, self.paginate_thread_by)
        page = self.request.GET.get('page')
        threads = paginator.get_page(page)

        # get chosen thread and beloning messages
        print(self.kwargs['thread_id'])
        if int(self.kwargs['thread_id']) != 0:
            chosen_thread_id = self.kwargs['thread_id']
            chosen_thread = Thread.objects.get(pk=chosen_thread_id)
            messages = Message.objects.filter(thread__id=chosen_thread_id)
            context['messages'] = messages
            context['chosen_thread'] = chosen_thread

        # get thread and message forms
        thread_form = ThreadForm
        message_form = MessageForm

        context['feeds'] = feeds
        context['group_channels'] = group_channels
        context['common_channels'] = common_channels
        context['threads'] = threads
        context['chosen_channel_id'] = chosen_channel_id
        context['chosen_channel'] = chosen_channel
        context['is_paginated'] = paginator.num_pages > 1
        context['thread_form'] = thread_form
        context['message_form'] = message_form
        return context


# View for creating new Channels
class CreateChannelView(LoginRequiredMixin, FormView):
    model = Channel
    template_name = "nablaforum/create_channel.html"
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
            new_channel.members.add(self.request.user)
            new_channel.save()
            first_thread = Thread.objects.create(

                                            channel=new_channel,
                                            threadstarter=self.request.user,
                                            title="Velkommen til " + new_channel.name,
                                            text="Dette en tråd!")
        except:
            print('Ops! Kunne ikke opprette kanal, ugyldig verdi i feltene!')
        return redirect('forum-main', channel_id=1, thread_id=0)

'''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        query_set = Channel.objects.filter(group__in=user.groups.all()).order_by('-pk') # All channels belonging to users group
        pinned_channels = query_set.filter(is_pinned=True) # pinned channels
        common_channels = self.model.objects.filter(group=None).filter(members=self.request.user) # channels common to all NablaUsers
        feeds = Channel.objects.filter(is_feed=True)# feeds

        # Find all channels with unreads and sets channel.has_unreads to True
        # Was not able to figure out a more django way to do this :(
        for channel in query_set:
            for thread in Thread.objects.filter(channel=channel):
                if Message.objects.filter(thread=thread).exclude(read_by_user=self.request.user):
                    channel.has_unreads = True
                    break

        for channel in common_channels:
            for thread in Thread.objects.filter(channel=channel):
                if Message.objects.filter(thread=thread).exclude(read_by_user=self.request.user):
                    channel.has_unreads = True
                    break

        paginator = Paginator(query_set, self.paginate_by)
        page = self.request.GET.get('page')
        group_channels = paginator.get_page(page)
        context['channel_types'] = {"Feeds": feeds,
                                    "Ordinære kanaler": common_channels,
                                    "Kullgruppe": pinned_channels,
                                    "Dine gruppers kanaler": group_channels}

        context['is_paginated'] = paginator.num_pages > 1
        return context
'''


# Convert to Formview and do it with django form
class BrowseChannelsView(LoginRequiredMixin, FormView):
    '''View for browsing channels'''
    form_class = JoinChannelsForm
    template_name = 'nablaforum/browse_channels.html'


    def form_valid(self, form):
        form_data = form.cleaned_data # selected channels
        channel_names = form_data['selected_channels']
        joinable_channels = Channel.objects.filter(group=None).exclude(members=self.request.user)
        for name in channel_names:
            channel = joinable_channels.get(name=name)
            channel.members.add(self.request.user)
        return redirect('forum-main', channel_id=1, thread_id=0)


    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        channels = Channel.objects.filter(group=None).exclude(members=self.request.user)
        kwargs['selected_channels'] = [(c, c.name) for c in channels]
        return kwargs



from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, CreateView
from django.views.generic.list import MultipleObjectMixin
from django.core.paginator import Paginator

from .models import Channel, Thread, Message
from .forms import ThreadForm, MessageForm, ChannelForm
from nablapps.accounts.models import NablaGroup


''' Should make  every new channel with a welcome thread '''


# View for displaying Channels
class IndexView(LoginRequiredMixin, FormView):
    model = Channel
    template_name = "nablaforum/index.html"
    form_class = ChannelForm
    paginate_by = 10


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
            first_thread = Thread.objects.create(

                                            channel=new_channel,
                                            threadstarter=self.request.user,
                                            title="Velkommen til " + new_channel.name,
                                            text="Dette en tråd!")
        except:
            print('Ops! Kunne ikke opprette kanal, ugyldig verdi i feltene!')
        # return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        query_set = Channel.objects.filter(group__in=user.groups.all()).order_by('-pk') # All channels belonging to users group
        pinned_channels = query_set.filter(is_pinned=True) # pinned channels
        common_channels = self.model.objects.filter(is_common=True) # channels common to all NablaUsers
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
        channels = paginator.get_page(page)
        context['channel_types'] = {"Feeds": feeds,
                                    "Felleskanaler": common_channels,
                                    "Kullgruppe": pinned_channels,
                                    "Dine gruppers kanaler": channels}

        context['is_paginated'] = paginator.num_pages > 1
        print(feeds)
        return context


# View for displaying Threads in a channel
class ChannelIndexView(LoginRequiredMixin, FormView):
    model = Thread
    template_name = "nablaforum/channel.html"
    form_class = ThreadForm
    paginate_by = 10


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
        query_set = self.model.objects.filter(channel__id=channel_id).order_by('-pk')

        for thread in query_set:
            if Message.objects.filter(thread=thread).exclude(read_by_user=self.request.user): # set of undread messages in a thread
                thread.has_unreads = True

        paginator = Paginator(query_set, self.paginate_by)
        page = self.request.GET.get('page')
        threads = paginator.get_page(page)
        context['threads'] = threads
        context['channel_id'] = channel_id
        context['channel'] = channel
        context['is_paginated'] = paginator.num_pages > 1
        return context


# View for displaying messages in a thread
class ThreadView(LoginRequiredMixin, MultipleObjectMixin, CreateView):
    model = Message
    template_name = "nablaforum/thread.html"
    fields = ['message']
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.thread_id = kwargs['thread_id']
        self.thread = get_object_or_404(Thread, pk=self.thread_id)
        self.channel_id = kwargs['channel_id']
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.thread.message_set.order_by('created')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.thread = self.thread
        self.object.user = self.request.user
        self.object.save()
        self.object.read_by_user.add(self.request.user)

        form = self.get_form_class() # Clean form for writing new message
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = {}
        self.object_list = self.get_queryset()
        # Each message in the view is now read by the user
        for message in self.object_list:
            message.read_by_user.add(self.request.user)
        context['thread'] = self.thread
        context['channel_id'] = self.channel_id
        print("context channel_id: ", "|" + context['channel_id'] + "|")
        return super().get_context_data(**context, **kwargs)

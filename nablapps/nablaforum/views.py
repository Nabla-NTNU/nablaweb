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

class GenericNameToBeChangedView(LoginRequiredMixin, MultipleObjectMixin, CreateView):
    """
    model               : model to be listed/created
    template_name
    fields              : fields of ::model to be included in form
    paginate_by
    context_object_name : name of object_list in context
    """
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        """
        try:  # Assume ThreadView
            self.thread_id = kwargs['thread_id']
            self.thread = get_object_or_404(Thread, pk=self.thread_id)
        except KeyError:  # No thread_id => we are in ChannelView
            self.channel_id = kwargs['channel_id']
            self.channel = get_object_or_404(Channel, pk=self.channel_id)
        """
        self.channel_id = kwargs['channel_id']
        self.container_name = self.container.__name__.lower()
        setattr(self, self.container_name+"_id", kwargs[self.container_name+"_id"])
        container_object = get_object_or_404(self.container, pk=getattr(self, self.container_name+"_id"))
        setattr(self, self.container_name, container_object)
        return super().dispatch(request, *args, **kwargs)

    def _pre_save(self):
        pass

    def _post_save(self):
        pass

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self._pre_save()
        self.object.save()
        self._post_save()

        form = self.get_form_class() # Clean input field in order to be ready for new input
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = {}
        self.object_list = self.get_queryset()
        context["channel_id"] = self.channel_id
        context[self.container_name] = getattr(self, self.container_name)
        return super().get_context_data(**context, **kwargs)

class ChannelView(GenericNameToBeChangedView):
    context_object_name = "thread_list"
    fields = ["title", "text"]
    model = Thread
    container = Channel
    template_name = "nablaforum/channel.html"

    def get_queryset(self):
        return self.channel.thread_set.order_by('-pk')

    def _pre_save(self):
        self.object.channel = self.channel
        self.object.threadstarter = self.request.user

class ThreadView(GenericNameToBeChangedView):
    context_object_name = "message_list"
    fields = ['message']
    model = Message
    template_name = "nablaforum/thread.html"
    container = Thread

    def get_queryset(self):
        return self.thread.message_set.order_by('created')

    def _pre_save(self):
        self.object.thread = self.thread
        self.object.user = self.request.user

    def _post_save(self):
        self.object.read_by_user.add(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for message in self.object_list:
            message.read_by_user.add(self.request.user)
        return context

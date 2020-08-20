from itertools import chain

from django.contrib import messages as django_messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import FormView, TemplateView

from nablapps.accounts.models import NablaGroup

from .forms import ChannelForm, JoinChannelsForm, MessageForm, ThreadForm
from .models import Channel, Message, Thread


class MainView(LoginRequiredMixin, TemplateView):
    """ Main view displaying forum content """

    template_name = "nablaforum/forum.html"
    paginate_thread_by = 5

    def post(self, request, **kwargs):
        thread_form = ThreadForm(self.request.POST)
        message_form = MessageForm(self.request.POST)

        if thread_form.is_valid():
            form_data = thread_form.cleaned_data
            channel_id = self.kwargs["channel_id"]
            channel = Channel.objects.get(pk=channel_id)
            if not channel.is_feed:
                try:
                    new_thread = Thread.objects.create(
                        channel=channel,
                        threadstarter=self.request.user,
                        title=form_data["title_field"],
                        text=form_data["text_field"],
                    )

                    new_message = Message.objects.create(
                        thread=new_thread, user=self.request.user, message=new_thread.text
                    )
                    new_message.read_by_user.add(self.request.user)
                except:  # noqa: E722
                    django_messages.add_message(
                        self.request,
                        django_messages.INFO,
                        "Ops! Kunne ikke opprette tråd, ugyldig verdi i feltene!",
                    )
                return redirect("forum-main", channel_id=channel_id, thread_id=0)
            else:
                # In the unlikely event that somone without permission sends a valid post
                # request, despite the form not being rendered
                django_messages.add_message(
                    self.request,
                    django_messages.INFO,
                    "Brukeren din har ikke tillatelse til å opprette ny tråd i nablafeed.",
                )
                return redirect("forum-main", channel_id=channel_id, thread_id=0)

        elif message_form.is_valid():
            form_data = message_form.cleaned_data
            thread_id = self.kwargs["thread_id"]
            channel_id = self.kwargs["channel_id"]
            thread = get_object_or_404(Thread, pk=thread_id)
            try:
                new_message = Message.objects.create(
                    thread=thread,
                    user=self.request.user,
                    message=form_data["message_field"],
                )
                new_message.read_by_user.add(self.request.user)
            except:  # noqa: E722
                django_messages.add_message(
                    self.request,
                    django_messages.INFO,
                    "Ops! Kunne ikke opprette melding, ugyldig verdi i feltene!",
                )
            return redirect("forum-main", channel_id=channel_id, thread_id=thread_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # All channels belonging to users group
        group_channels = (
            Channel.objects.filter(group__in=user.groups.all())
            .exclude(is_class=True)
            .order_by("-pk")
        )

        # Ordinary channels the user is member of
        common_channels = (
            Channel.objects.filter(group=None)
            .filter(members=self.request.user)
            .exclude(is_feed=True)
            .exclude(is_class=True)
        )

        # Class channel
        class_channel = Channel.objects.filter(group__in=user.groups.all()).filter(
            is_class=True
        )

        # Feeds
        feeds = Channel.objects.filter(is_feed=True)

        # get chosen channel and belonging threads
        chosen_channel_id = self.kwargs["channel_id"]
        chosen_channel = Channel.objects.get(pk=chosen_channel_id)
        channel_threads = Thread.objects.filter(channel__id=chosen_channel_id).order_by(
            "-pk"
        )
        paginator = Paginator(channel_threads, self.paginate_thread_by)
        page = self.request.GET.get("page")
        threads = paginator.get_page(page)

        # get chosen thread and beloning messages
        print(self.kwargs["thread_id"])
        if int(self.kwargs["thread_id"]) != 0:
            chosen_thread_id = self.kwargs["thread_id"]
            chosen_thread = Thread.objects.get(pk=chosen_thread_id)
            messages = Message.objects.filter(thread__id=chosen_thread_id)

            for message in messages.exclude(read_by_user=self.request.user):
                message.read_by_user.add(self.request.user)

            context["first_message"] = messages[0]
            context["messages"] = messages[
                1:
            ]  # All messages except the first which is the same as thread.text
            context["chosen_thread"] = chosen_thread

        # get thread and message forms
        thread_form = ThreadForm
        message_form = MessageForm

        # Check for unreads messages within the last week
        one_week_ago = timezone.now() - timezone.timedelta(days=7)

        # Check for channels with unreads
        all_users_channels = chain(feeds, group_channels, common_channels)
        for channel in all_users_channels:
            for thread in Thread.objects.filter(channel=channel):
                if Message.objects.filter(
                    thread=thread, created__gte=one_week_ago
                ).exclude(read_by_user=self.request.user):
                    print(thread)
                    channel.has_unreads = True
                    break

        # Check unreads for threads in chosen channel
        for thread in threads:
            if Message.objects.filter(thread=thread, created__gte=one_week_ago).exclude(
                read_by_user=self.request.user
            ):
                thread.has_unreads = True

        context["feeds"] = feeds
        context["class_channel"] = class_channel
        context["group_channels"] = group_channels
        context["common_channels"] = common_channels
        context["threads"] = threads
        context["chosen_channel_id"] = chosen_channel_id
        context["chosen_channel"] = chosen_channel
        context["is_paginated"] = paginator.num_pages > 1
        context["thread_form"] = thread_form
        context["message_form"] = message_form
        return context


class CreateChannelView(LoginRequiredMixin, FormView):
    """ View for creating new channels """

    model = Channel
    template_name = "nablaforum/create_channel.html"
    form_class = ChannelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["groups"] = NablaGroup.objects.filter(
            pk__in=self.request.user.groups.all().values_list("pk")
        )
        return kwargs

    def form_valid(self, form):
        form_data = form.cleaned_data
        try:
            new_channel = self.model.objects.create(
                group=form_data["group"],
                name=form_data["name"],
                description=form_data["description"],
            )
            new_channel.members.add(self.request.user)
            new_channel.save()
        except:  # noqa: E722
            django_messages.add_message(
                self.request,
                django_messages.INFO,
                "Ops! Kunne ikke opprette melding, ugyldig verdi i feltene!",
            )
        return redirect("forum-main", channel_id=1, thread_id=0)


class BrowseChannelsView(LoginRequiredMixin, FormView):
    """View for browsing channels"""

    form_class = JoinChannelsForm
    template_name = "nablaforum/browse_channels.html"

    def form_valid(self, form):
        form_data = form.cleaned_data  # selected channels
        channel_names = form_data["selected_channels"]
        joinable_channels = (
            Channel.objects.filter(group=None)
            .exclude(members=self.request.user)
            .exclude(is_feed=True)
        )
        for name in channel_names:
            channel = joinable_channels.get(name=name)
            channel.members.add(self.request.user)
        return redirect("forum-main", channel_id=1, thread_id=0)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        channels = (
            Channel.objects.filter(group=None)
            .exclude(members=self.request.user)
            .exclude(is_feed=True)
        )
        kwargs["selected_channels"] = [(c, c.name) for c in channels]
        return kwargs

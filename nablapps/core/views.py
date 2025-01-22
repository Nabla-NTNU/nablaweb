"""
Core views in nablaweb
"""

from datetime import datetime, timedelta
from itertools import chain

from django.contrib import messages
from django.utils import timezone
from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin

from nablapps.album.models import Album
from nablapps.blog.models import BlogPost

from ..accounts.models import FysmatClass
from ..events.models import Event, EventRegistration
from ..nabladet.models import Nablad
from ..nablaforum.models import Channel, Message, Thread
from ..news.models import FrontPageNews
from ..officeCalendar.models import OfficeEvent
from ..podcast.models import Podcast
from ..poll.models import Poll
from .view_mixins import FlatPageMixin


def get_year_for_leaderboard():
    """
    Gets the year for making the bedpres leaderboard.
    Return current year if date after 15.07, else the previous year.
    """
    cur_date = datetime.now()
    year = cur_date.year
    if cur_date < datetime(year, 7, 15):
        return year - 1
    else:
        return year


class FrontPageView(FlatPageMixin, TemplateView):
    """
    The view for showing the front page of nablaweb
    """

    template_name = "front_page.html"
    flatpages = [
        ("frontpageinfo", "/forsideinfo/"),
        ("sidebarinfo", "/sidebarinfo/"),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs
        )  # Inject complicated context. # This context processing should perhaps be moved to the corresponding apps. self._add_news(context)
        self._add_events_and_bedpres(context)
        self._add_poll(context)
        self._add_nablad(context)
        self._add_podcast(context)
        self._add_forum(context)
        context["office_events"] = OfficeEvent.get_office_event_week(
            only_public=not self.request.user.is_authenticated
        )
        context["new_podcast"] = (
            Podcast.objects.exclude(is_clip=True)
            .filter(pub_date__lte=datetime.now())
            .first()
        )
        context["album_list"] = Album.objects.exclude(visibility="h").order_by(
            "-last_changed_date"
        )[:4]
        context["new_blog"] = BlogPost.objects.exclude(list_image=None).order_by(
            "-created_date"
        )[:4]
        context["newuser_message"] = (
            False if self.request.user.is_authenticated else True
        )
        context["logged_in"] = True if self.request.user.is_authenticated else False
        # Uncomment when fadderperiode to display new student popup.
        # context["newuser_popup"] = False if self.request.user.is_authenticated else True

        context["bedpres_leaderboard"] = EventRegistration.objects.raw(
            f"""SELECT 1 as id,
                  COUNT(r.attendance_registration) AS num_bedpres,
                  u.username,
                  u.first_name, u.last_name
                FROM content_eventregistration AS r
                INNER JOIN accounts_nablauser AS u ON r.user_id = u.id
                INNER JOIN content_event AS e ON r.event_id = e.id
                WHERE r.date > '{get_year_for_leaderboard()}-07-15'
                  AND r.date < '{int(get_year_for_leaderboard()) + 1}-07-15'
                  AND e.is_bedpres = 1
                GROUP BY r.user_id
                ORDER BY num_bedpres DESC
                LIMIT 10"""
        )
        return context

    def _add_news(self, context):
        news_list = FrontPageNews.objects.filter(visible=True).filter(
            bump_time__lte=datetime.now()
        )
        context["main_news"] = news_list.first()
        context["news_list"] = news_list[1:7]

    def _add_nablad(self, context):
        context["new_nablad"] = Nablad.objects.order_by("-pub_date")[:1]
        if not self.request.user.is_authenticated:
            context["new_nablad"] = Nablad.objects.exclude(is_public=False).order_by(
                "-pub_date"
            )[:1]

    def _add_podcast(self, context):
        context["new_podcast_list"] = (
            Podcast.objects.exclude(is_clip=True)
            .filter(pub_date__lte=datetime.now())
            .order_by("-pub_date")[:4]
        )

    def _add_events_and_bedpres(self, context):
        now = datetime.now() - timedelta(hours=6)
        context["upcoming_events"] = (
            Event.objects.filter(event_start__gte=now)
            .exclude(is_bedpres=True)
            .order_by("event_start")[:5]
        )
        context["upcoming_bedpreses"] = Event.objects.filter(
            event_start__gte=now, is_bedpres=True
        ).order_by("event_start")[:5]

    def _add_poll(self, context):
        try:
            context["poll"] = Poll.objects.current_poll()
        except Poll.DoesNotExist:
            context["poll"] = (
                Poll.objects.exclude(is_user_poll=True)
                .order_by("-publication_date")
                .first()
            )

        if self.request.user.is_authenticated and context["poll"] is not None:
            context["poll_has_voted"] = context["poll"].user_has_voted(
                self.request.user
            )

    def _add_forum(self, context):
        if self.request.user.is_authenticated:
            # Check for unread messages in users channels
            new_forum_messages = False

            user = self.request.user
            one_week_ago = timezone.now() - timezone.timedelta(days=7)

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

            # Feeds
            feeds = Channel.objects.filter(is_feed=True)

            all_users_channels = chain(feeds, group_channels, common_channels)
            for channel in all_users_channels:
                if new_forum_messages:
                    break
                for thread in Thread.objects.filter(channel=channel):
                    if Message.objects.filter(
                        thread=thread, created__gte=one_week_ago
                    ).exclude(read_by_user=self.request.user):
                        new_forum_messages = True
                        break
            context["new_forum_messages"] = new_forum_messages

            if FysmatClass.objects.filter(user=self.request.user).exists():
                # If multiple classes, use first entry
                fysmat_class = FysmatClass.objects.filter(
                    user=self.request.user
                ).first()
                class_channel, created = Channel.objects.get_or_create(
                    group=fysmat_class, is_class=True, name=fysmat_class.name
                )
                latest_class = Thread.objects.filter(channel=class_channel).order_by(
                    "-pk"
                )[:4]
                context["fysmat_class"] = fysmat_class
                context["latest_class"] = latest_class
            else:
                messages.add_message(
                    self.request,
                    messages.INFO,
                    "Brukeren din er ikke tilknyttet noen kullgruppe. Ta kontakt med WebKom for å få det fikset.",
                )
            latest_feed = Thread.objects.filter(channel__is_feed=True).order_by("-pk")[
                :4
            ]
            context["latest_feed"] = latest_feed


class AboutView(TemplateView):
    template_name = "core/general_about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class InternView(LoginRequiredMixin, TemplateView):
    template_name = "intern.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self._add_polls(context)
        return context

    def _add_polls(self, context):
        polls = Poll.objects.order_by("-creation_date")[:6]
        has_voted_on = [poll.user_has_voted(self.request.user) for poll in polls]
        context["polls_context"] = zip(polls, has_voted_on)

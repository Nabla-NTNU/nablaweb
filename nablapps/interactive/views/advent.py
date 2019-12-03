from braces.views import PermissionRequiredMixin
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from nablapps.accounts.models import NablaUser
from time import mktime
from wsgiref.handlers import format_date_time
from django.core.exceptions import PermissionDenied

from ..models.advent import AdventCalendar, AdventDoor, AdventParticipation, SantaCount, Santa


class AdventDoorView(DetailView):
    model = AdventDoor
    pk_url_kwarg = "number"
    context_object_name = "door"

    def get_object(self, queryset=None):
        self.calendar = get_object_or_404(AdventCalendar, year=self.kwargs['year'])
        door = get_object_or_404(AdventDoor, number=self.kwargs['number'], calendar=self.calendar)
        if door.is_published or self.request.user.has_perm("interactive.change_adventdoor"):
            return door
        else:
            raise Http404("Ikke publisert")

    def get_template_names(self):
        return self.object.template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        door = self.object
        context['calendar'] = self.calendar
        try:
            user = self.request.user
            if not user.is_anonymous:
                context['part'] = AdventParticipation.objects.get(
                    user=user,
                    door=door.id
                )
        except AdventParticipation.DoesNotExist:
            pass
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if self.calendar.requires_login and not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        return response


class AdventCalendarView(ListView):
    model = AdventDoor
    context_object_name = "doors"

    def dispatch(self, request, *args, **kwargs):
        self.calendar = get_object_or_404(AdventCalendar, year=kwargs['year'])
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return self.calendar.template

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(calendar=self.calendar)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calendar'] = self.calendar
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        now = datetime.now()
        if now < datetime(now.year, now.month, now.day, 10):
            now = now - timedelta(days=1)
        next = datetime(now.year, now.month, now.day, 10) + timedelta(days=1)
        response['Cache-Control'] = "max-age=" \
                                    + str((next - now).seconds)
        stamp = mktime(next.timetuple())
        response['Expires'] = format_date_time(stamp)  # legacy support
        
        if self.calendar.requires_login and not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        
        return response


@login_required
def participate_in_competition(request, year, number):

    calendar = get_object_or_404(AdventCalendar, year=year)
    door = get_object_or_404(AdventDoor,
                             calendar=calendar,
                             number=number
                             )

    if door.is_lottery and door.is_today:
        user = request.user
        text = request.POST.get('text')
        AdventParticipation.objects.update_or_create(
            user=user,
            door=door,
            defaults={
                'text': text,
                'when': datetime.now()
            }
        )
    return redirect(door.get_absolute_url())


@permission_required("interactive.change_adventdoor")
def reset_door(request, year, number):
    calendar = get_object_or_404(AdventCalendar, year=year)
    door = get_object_or_404(AdventDoor,
                             calendar=calendar,
                             number=number
                             )
    my_next = request.GET.get('next')

    if door.is_today:
        door.winner = None
        door.save()
    return redirect(my_next)


class AdventDoorAdminView(PermissionRequiredMixin, DetailView):
    model = AdventDoor
    pk_url_kwarg = "number"
    context_object_name = "door"
    template_name = "interactive/advent_admin.html"
    permission_required = "interactive.change_adventdoor"

    def get_object(self, queryset=None):
        calendar = get_object_or_404(AdventCalendar, year=self.kwargs['year'])
        return get_object_or_404(AdventDoor, number=self.kwargs['number'], calendar=calendar)

    def post(self, *args, **kwargs):
        door = self.get_object()
        if door.winner:
            messages.info(self.request, "Vinner allerede valgt")
        elif door.is_text_response:
            try:
                winner_username = self.request.POST.get('winner')
                door.winner = NablaUser.objects.get(username=winner_username)
                door.save()
            except NablaUser.DoesNotExist:
                messages.error(self.request, "Ingen vinner valgt")
        else:
            door.choose_winner()
            door.save()
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['base_template'] = self.object.calendar.template

        return context

def register_found_santa(request, santa_id, redirect_url):
    if request.user.is_authenticated:
        santa_count, created = SantaCount.objects.get_or_create(user=request.user)
        santa = get_object_or_404(Santa, pk=santa_id)
        if santa.santa_location == redirect_url:
            if santa not in santa_count.santas.all():
                santa_count.santas.add(santa)
                santa_count.save()
    return redirect("hidden_santa")

class SantaCountListView(ListView):
    model = SantaCount
    template_name = "interactive/santa_hunt.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if(self.request.user.is_authenticated):
            try:
                user_count = SantaCount.objects.get(user=self.request.user)
                context["user_score"] = user_count.get_score()
            except:
                context["user_score"] = 0

        all_santa_counts = SantaCount.objects.all()
        all_santa_counts = sorted(all_santa_counts, key = lambda x: -x.get_score())

        users = []
        user_results = []

        for obj in all_santa_counts:
            users.append(obj.user.get_full_name())
            user_results.append(obj.get_score())

        santa_hunters = zip(users, user_results)
        context["santa_hunters"] = santa_hunters
        return context

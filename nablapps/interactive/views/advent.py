from django.views.generic import DetailView, ListView
from ..models.advent import AdventCalendar, AdventDoor, AdventParticipation
from nablapps.accounts.models import NablaUser
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from datetime import timedelta
from braces.views import PermissionRequiredMixin
from django.contrib import messages
from content.views.mixins import PublishedMixin
from wsgiref.handlers import format_date_time
from time import mktime


class AdventDoorView(PublishedMixin, DetailView):
    model = AdventDoor
    pk_url_kwarg = "number"
    context_object_name = "door"

    def get_object(self, queryset=None):
        calendar = get_object_or_404(AdventCalendar, year=self.kwargs['year'])
        door = get_object_or_404(AdventDoor, number=self.kwargs['number'], calendar=calendar)
        if door.is_published or self.request.user.has_perm("interactive.change_adventdoor"):
            return door
        else:
            raise Http404("Ikke publisert")

    def get_template_names(self):
        return self.object.template

    def get_context_data(self, **kwargs):
        context = super(AdventDoorView, self).get_context_data(**kwargs)
        door = self.object
        context['calendar'] = door.calendar
        try:
            user = self.request.user
            if not user.is_anonymous():
                context['part'] = AdventParticipation.objects.get(
                    user=user,
                    door=door.id
                )
        except AdventParticipation.DoesNotExist:
            pass
        return context


class AdventCalendarView(ListView):
    model = AdventDoor
    context_object_name = "doors"

    def dispatch(self, request, *args, **kwargs):
        self.calendar = AdventCalendar.objects.get(year=kwargs['year'])
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
        year = context['door'].calendar.year
        # TODO: gjør advent_base til advent_base_2015 og fiks default greien
        if year == 2015:
            context['base_template'] = "interactive/advent_base.html"
        else:
            context['base_template'] =  "interactive/advent_base_" + str(year) + ".html"
        return context

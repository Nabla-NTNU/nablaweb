from django.views.generic import DetailView, ListView
from interactive.models.advent import AdventCalendar, AdventDoor, AdventParticipation
from accounts.models import NablaUser
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from braces.views import PermissionRequiredMixin
from django.contrib import messages


class AdventDoorView(DetailView):
    model = AdventDoor
    pk_url_kwarg = "number"
    context_object_name = "door"

    def get_template_names(self):
        return self.object.template

    def get_context_data(self, **kwargs):
        context = super(AdventDoorView, self).get_context_data(**kwargs)
        door = context['door']
        context['calendar'] = door.calendar
        try:
            user = self.request.user
            context['part'] = AdventParticipation.objects.get(
                user=user,
                door=door
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
        queryset.filter(calendar=self.calendar)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calendar'] = self.calendar
        return context


@login_required
def participate_in_competition(request, year, number):

    calendar = AdventCalendar.objects.get(year=year)
    door = AdventDoor.objects.get(
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


@permission_required("interactive.adventdoor_change")
def reset_door(request, year, number):
    calendar = AdventCalendar.objects.get(year=year)
    door = AdventDoor.objects.get(
        calendar=calendar,
        number=number
    )
    next = request.GET.get('next')

    if door.is_today:
        door.winner = None
        door.save()
    return redirect(next)


class AdventDoorAdminView(PermissionRequiredMixin, DetailView):
    model = AdventDoor
    pk_url_kwarg = "number"
    context_object_name = "door"
    template_name = "interactive/advent_admin.html"
    permission_required = "interactive.adventdoor_change"

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

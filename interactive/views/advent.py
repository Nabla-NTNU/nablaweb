from django.views.generic import DetailView, ListView
from interactive.models import AdventCalendar, AdventDoor
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

class AdventDoorView(DetailView):
    model = AdventDoor
    pk_url_kwarg = "number"
    context_object_name = "door"

    def get_template_names(self):
        return self.object.template

    def get_context_data(self, **kwargs):
        context = super(AdventDoorView, self).get_context_data(**kwargs)
        context['calendar'] = context['door'].calendar
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


def participate_in_competition(request, year, number):

    user = request.user
    calendar = AdventCalendar.objects.get(year=year)

    if user.is_authenticated():
        door = AdventDoor.objects.get(
            calendar=calendar,
            door=number
        )
        if door.is_lottery() and user not in door.users:
            door.users.add(user)

        return redirect(door.get_absoulte_url())
    else:
        return redirect(reverse("auth_login"))

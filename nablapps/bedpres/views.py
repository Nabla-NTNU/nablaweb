"""
Views for bedpres app.

Should function mostly the same as the views in the events app,
and they are mostly just inherited versions of those in events.
"""
from django.http import HttpResponse
from django.template import loader
from nablapps.events.views import EventDetailView, RegisterUserView
from .bpcmixin import WrongClass
from .models import BedPres
from .utils import InvalidCardNum


class BedPresRegisterUserView(RegisterUserView):
    """
    View used by a user for registering for a Bedpres
    """
    model = BedPres

    def register_user(self, user):
        """
        Overridden method.
        We have to take care of the case that a user can lack a correct cardnumber.
        """
        try:
            return super().register_user(user)
        except InvalidCardNum:
            return "Du ble ikke påmeldt fordi brukeren din mangler gyldig NTNU-kortnummer. " \
                   "Rediger profilen din og prøv igjen"
        except WrongClass as e:
            if e.user.get_class_number() == 0:
                return (
                    "Du ble ikke påmeldt fordi du ikke er registrert på noe kull. "
                    "Send en epost til webkom@nabla.ntnu.no for å fikse det.")
            return (
                "Du ble ikke påmeldt fordi du går i feil klasse for dette arrangementet.\n"
                f"I følge våre systemer går du i {e.user.get_class_number()}. klasse "
                f"og arrangementet er kun åpent for {e.event.bpc_event.min_year}. "
                f"til {e.event.bpc_event.max_year}. klasse.")


class BedPresDetailView(EventDetailView):
    """Show a single Bedpres"""
    model = BedPres
    template_name = 'bedpres/bedpres_detail.html'
    context_object_name = "bedpres"


def ical_event(request, event_id):
    """Returns a given event or bedpres as an iCal .ics file"""

    event = BedPres.objects.get(id=event_id)

    # Use the same template for both Event and BedPres.
    template = loader.get_template('events/event_icalendar.ics')
    context = {'event_list': (event,), }
    response = HttpResponse(template.render(context), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=Nabla_%s.ics' % event.slug
    return response

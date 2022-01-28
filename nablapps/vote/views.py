import json
from itertools import chain
from random import shuffle

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt  # TODO: remove
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.detail import BaseDetailView

from nablapps.accounts.models import NablaUser

from .forms import AlternativeFormset
from .models import (
    Alternative,
    DuplicatePriorities,
    HoleInBallotError,
    UserAlreadyVoted,
    UserNotCheckedIn,
    UserNotEligible,
    Voting,
    VotingDeactive,
    VotingEvent,
)

####################
### Admin views ####
####################


# TODO fix permissions
# TODO Several of the API endpoints, especially the post, should have more error handling.
#      Right now we will get 500 for invalid requests.


def _attendance_response(error=None, user=None, is_checked_in=None):
    """Generates the object used to report the success/failure of attendance registration"""
    return {
        "error": error,
        "user": user,
        "is_checked_in": is_checked_in,
    }


def register_attendance(event, user_pk, action):
    """Check in/out user from a voting event.
    Verify that the user i eligable, and then perform the checkin.
    Return a status.

    GET paramters:
      action: String - one of 'toggle', 'in', 'out', 'nothing'. Default: 'toggle'

    Response:
      Json with the currently attending users."""

    user = NablaUser.objects.get(pk=user_pk)
    actions = {
        "toggle": event.toggle_check_in_user,
        "in": event.check_in_user,
        "out": event.check_out_user,
        "nothing": lambda user: None,
    }

    try:
        action_func = actions[action]
        action_func(user)
    except KeyError:
        return _attendance_response(
            error=f"Invalid action '{action}'. Must be one of {actions.keys}"
        )
    except UserNotEligible:
        return _attendance_response(error="User is not eligible for this event")

    return _attendance_response(
        user=_user_serializer(user), is_checked_in=event.user_checked_in(user)
    )


def _register_attendance_card(event, rfid_number, action):
    """Register attendance using card as identifyer

    Throws:
     - NablaUser.DoesNotExist if the card does not correspond to a user"""
    try:
        user = NablaUser.objects.get_from_rfid(rfid_number)
    except ValueError as e:  # Thrown by invalid card numbers
        if "invalid literal for int() with base 10:" in str(e):
            raise NablaUser.DoesNotExist("Invalid card format. No user.")
        else:
            raise e
    # get_from_rfid does no throw exception if nothing is found, it is simply None if none found
    if user is None:
        raise NablaUser.DoesNotExist("Unknown card")
    return register_attendance(event, user.pk, action)


def _register_attendance_username(event, username, action):
    """Register attendance using username as identifyer"""
    # TODO: something with exceptions
    user = NablaUser.objects.get(username=username)
    return register_attendance(event, user.pk, action)


def register_attendance_any_identifier(event, identifier, action):
    """Register attendance, attempting several identifiers"""
    # Prioritized list of identifiers
    identifiers = [
        {"name": "card", "function": _register_attendance_card},
        {"name": "username", "function": _register_attendance_username},
        # Do not include pk, as it we feel it is bad practice to allow using a sequential identifier.
    ]

    for identifier_type in identifiers:
        try:
            return identifier_type["function"](event, identifier, action)
        except NablaUser.DoesNotExist:  # Procede to next identifier
            pass
    return _attendance_response(
        error="User not found, tried to match with "
        + ", ".join([i["name"] for i in identifiers]),
    )


@method_decorator(csrf_exempt, name="dispatch")  # TODO: Remove this, for tesing only
class VoteAdminMixin(PermissionRequiredMixin):
    """Permission mixin for all admin views of vote."""

    def get_permission_required(self):
        get_perms = ("vote.vote_inspector",)
        post_perms = ("vote.vote_admin",)
        if self.request.method == "GET":
            return get_perms
        elif self.request.method == "POST":
            return post_perms
        else:
            raise ImproperlyConfigured("Method not supported")


def _user_serializer(user):
    """Returns a dictionary representing a user, for a JSON response"""
    return {
        "username": user.username,
        "name": user.get_full_name(),
    }


def _alternative_serializer(alternative):
    return {
        "pk": alternative.pk,
        "text": alternative.text,
        "votes": alternative.votes,
        "percentage": alternative.get_vote_percentage(),
    }


def _voting_serializer(voting, include_alternatives=True):
    response = {
        "pk": voting.pk,
        "title": voting.title,
        "active": voting.is_active,
        "num_voted": voting.get_total_votes(),
        "num_winners": voting.num_winners,
        # If created_by is empty, assume it was created through admin
        # interface, and thus we do not know who made it.
        "created_by": getattr(voting.created_by, "username", "Admin (aka unknown)"),
    }
    if include_alternatives:
        response["alternatives"] = [
            _alternative_serializer(a) for a in voting.alternatives.all()
        ]
    return response


class UsersAPIView(VoteAdminMixin, BaseDetailView):
    """API view for retrieving and updating logged in users

    Response form:
    {
        "users": [
            {"username": ..., ""},
        ],
        // If POST request, also include the following
        "lastAction": {
            "error": "",  // If empty, success
            "user": {"username": ..., ""},
            "is_checked_in": Bool,
        }
    }
    """

    model = VotingEvent

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        users = self.object.checked_in_users.all()
        return JsonResponse({"users": [_user_serializer(user) for user in users]})

    def post(self, request, *args, **kwargs):
        """Post request handler"""
        self.object = self.get_object()
        data = json.loads(request.body)
        # TODO: can extend the functionality to cycle through
        # several possible identifiers, such as ID card, username, etc.

        # TODO: exception handling
        username = data.get("username")
        action = data.get("action")
        attendence_reponse = register_attendance_any_identifier(
            self.object, username, action
        )
        print(username)
        print(attendence_reponse)
        users = self.object.checked_in_users.all()

        return JsonResponse(
            {
                "users": [_user_serializer(user) for user in users],
                "lastAction": attendence_reponse,
            }
        )


class VoteEventAPIView(VoteAdminMixin, BaseDetailView):
    """API view for getting information about voting event"""

    model = VotingEvent

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return JsonResponse(
            {
                "title": self.object.title,
                "eligile_group": self.object.eligible_group,
            }
        )


class VotingsAPIView(VoteAdminMixin, BaseDetailView):
    """API view for getting votings belonging to a voting event"""

    model = VotingEvent

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        votings = self.object.votings.all()
        return JsonResponse(
            {
                "votings": [_voting_serializer(voting) for voting in votings],
            }
        )

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        to_change = Voting.objects.get(pk=data.get("pk"))
        to_change.is_active = data.get("active")
        to_change.save()
        return self.get(request, *args, **kwargs)


class RegisterAttendanceView(VoteAdminMixin, DetailView):
    model = VotingEvent
    template_name = "vote/register_attendance2.html"


class VotingEventList(VoteAdminMixin, ListView):
    model = VotingEvent
    template_name = "vote/voting_event_list.html"

    def has_permission(self):
        perms = self.get_permission_required()
        for perm in perms:
            if self.request.user.has_perm(perm):
                return True
        return False


class VotingList(VoteAdminMixin, DetailView):
    """List of all votings in a voting event"""

    model = VotingEvent
    template_name = "vote/voting_list.html"

    def has_permission(self):
        perms = self.get_permission_required()
        for perm in perms:
            if self.request.user.has_perm(perm):
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_admin"] = self.request.user.has_perm("vote.vote_admin")
        return context


class CreateVoting(VoteAdminMixin, CreateView):
    """View for creating new votings"""

    permission_required = "vote.vote_admin"
    template_name = "vote/voting_form.html"
    model = Voting
    fields = ["event", "title", "num_winners", "description"]

    def get_initial(self):
        event_id = self.kwargs["pk"]
        event = get_object_or_404(VotingEvent, pk=event_id)
        return {
            "event": event,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs["pk"]
        context["event_id"] = event_id
        if self.request.POST:
            context["alternatives"] = AlternativeFormset(self.request.POST)
        else:
            context["alternatives"] = AlternativeFormset()
        return context

    def form_valid(self, form, **kwargs):
        """Called if all forms are valid. Creates voting and associated alternatives"""
        context = self.get_context_data()
        alternatives = context["alternatives"]
        event_id = self.kwargs["pk"]
        with transaction.atomic():
            self.object = form.save()
            if alternatives.is_valid():
                alternatives.instance = self.object
                event_id = alternatives.instance.event.pk
                alternatives.save()
        return redirect("voting-list", pk=event_id)
        return super().form_valid(form)


class VotingEdit(VoteAdminMixin, UpdateView):
    permission_required = "vote.vote_admin"
    model = Voting
    template_name = "vote/edit_voting.html"
    fields = ["event", "title", "description"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["alternatives"] = AlternativeFormset(self.request.POST)
        else:
            context["alternatives"] = AlternativeFormset()
        return context

    def form_valid(self, form, **kwargs):
        """Called if all forms are valid. Creates voting and associated alternatives"""
        if self.object.get_total_votes() == 0:
            context = self.get_context_data()
            alternatives = context["alternatives"]
            with transaction.atomic():
                self.object = form.save()
                if alternatives.is_valid():
                    alternatives.instance = self.object
                    alternatives.save()
            return redirect("voting-detail", pk=self.kwargs["pk"])
        else:
            messages.error(
                self.request,
                "OBS! Denne avstemningen har allerede blitt stemt på, endring ikke gyldig",
            )
            return redirect("voting-detail", pk=self.kwargs["pk"])


class VotingDetail(VoteAdminMixin, DetailView):
    """Display details such as alternatives and results"""

    permission_required = ("vote.vote_admin", "vote.vote_inspector")
    model = Voting
    template_name = "vote/voting_detail.html"

    def has_permission(self):
        perms = self.get_permission_required()
        for perm in perms:
            if self.request.user.has_perm(perm):
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_admin"] = self.request.user.has_perm("vote.vote_admin")

        if self.request.method == "POST":
            context["winners"] = self.object.get_multi_winner_result()
            print(self.object.get_multi_winner_result())
        else:
            self.object.multi_winnner_initial_dist()
        if self.object.num_winners > 1:
            context["quota"] = (
                int(self.object.get_total_votes() / (self.object.num_winners + 1)) + 1
            )
        return context

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@login_required
@permission_required("vote.vote_admin", raise_exception=True)
def get_multi_winner_result(request):
    pass


@login_required
@permission_required("vote.vote_admin", raise_exception=True)
def activate_voting(request, pk, redirect_to):
    """Open voting"""
    voting = Voting.objects.get(pk=pk)
    voting.is_active = True
    voting.save()
    return redirect(redirect_to)


@login_required
@permission_required("vote.vote_admin", raise_exception=True)
def deactivate_voting(request, pk, redirect_to):
    """Close voting"""
    voting = Voting.objects.get(pk=pk)
    voting.is_active = False
    voting.save()
    return redirect(redirect_to)


###########################################
### Non admin views, only login required ###
###########################################
def _alternative_public_serializer(alternative):
    return {
        "pk": alternative.pk,
        "text": alternative.text,
    }


def _voting_public_serializer(voting, user, include_alternatives=True):
    response = {
        "pk": voting.pk,
        "title": voting.title,
        "active": voting.is_active,
        "has_voted": voting.user_already_voted(user),
        "num_winners": voting.num_winners,
    }
    if include_alternatives:
        response["alternatives"] = [
            _alternative_public_serializer(a) for a in voting.alternatives.all()
        ]
    return response


@method_decorator(csrf_exempt, name="dispatch")  # TODO: Remove this, for tesing only
class VotingsPublicAPIView(LoginRequiredMixin, BaseDetailView):
    """API endpoint for votings with only 'public' information, i.e. not including number of votes etc.

    POST submit a vote
     {'alternative_pk': ...}

    Discussion:
     Could probably merge this with VotingsAPIView, and dynamically include/exclude data depending on permissions
     or something similar.
     However, I did not bother.
     Feel free to do so if you want.
    """

    model = VotingEvent

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        votings = self.object.votings.filter(is_active=True)
        return JsonResponse(
            {
                "votings": [
                    _voting_public_serializer(voting, request.user)
                    for voting in votings
                ],
                "should_poll": self.object.users_should_poll,
            }
        )

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            alternative_pk = data.get("alternative_pk")
            alternative = Alternative.objects.get(pk=alternative_pk)
        except KeyError as e:
            # Invlaid pk
            raise e
        except Alternative.DoesNotExist as e:
            raise e

        try:
            alternative.add_vote(request.user)
        except (UserNotCheckedIn, UserAlreadyVoted, UserNotEligible) as e:
            return JsonResponse({"error": str(e)}, status=403)  # 403 FORBIDDEN
        return self.get(request, *args, **kwargs)


class VotingEventUserView(LoginRequiredMixin, DetailView):
    """Collection of all votings for a given voting event"""

    model = VotingEvent
    template_name = "vote/voting_event_user_view.html"


class ActiveVotingList(LoginRequiredMixin, ListView):
    """Display list of active votings"""

    model = Voting
    template_name = "vote/active_voting_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        admin_rights = ["vote.vote_admin", "vote.vote_inspector"]
        context["admin_rights"] = any(
            [self.request.user.has_perm(right) for right in admin_rights]
        )
        return context

    def get_queryset(self):
        all_user_votings = self.model.objects.exclude(is_active=False).filter(
            event__eligible_group=None
        )
        user_group_votings = self.model.objects.exclude(is_active=False).filter(
            event__eligible_group__in=self.request.user.groups.all()
        )
        return chain(all_user_votings, user_group_votings)


class Vote(LoginRequiredMixin, DetailView):
    """
    Display alternatives and lets users vote

    The form for voting is a little shabby(TM),
    probably smoother with formset. Didn't want to bother with big rewrite,
    so leaving that for future-improvement(TM) :^)

    The creation of the Ballot (container and entries) can probably also be
    written in a much nicer way. I think ultimately if all votations in the future will
    be using STV, then this view as a CreateView together with a formset for the
    priorities/alternatives is probably nice.

    Disclaimer: possible misuse of docstring
    Disclaimer2: possible misuse of the (TM) joke
    """

    model = Voting
    template_name = "vote/voting_vote.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        alternatives = self.object.alternatives.all()
        alternatives = [alt for alt in alternatives]
        shuffle(alternatives)
        context["randomized_alternatives"] = alternatives
        context["has_voted"] = self.object.user_already_voted(self.request.user)
        context["priorities"] = [
            i for i in range(1, self.object.get_num_alternatives() + 1)
        ]
        return context

    def post(self, request, **kwargs):
        """Submit a vote from chosen alternative"""
        voting_id = kwargs["pk"]
        voting = get_object_or_404(Voting, pk=voting_id)

        if voting.num_winners > 1:
            # Single transferable vote
            # Get list/dictonary of alternatives and priorities
            try:
                priorities = [i for i in range(1, voting.get_num_alternatives() + 1)]
                # ballot : {pri#:alternative.pk}
                ballot_dict = {}
                for pri in priorities:
                    try:
                        ballot_dict[pri] = request.POST["priority" + str(pri)]
                        if pri > 1:
                            if ballot_dict[pri - 1] is None:
                                raise HoleInBallotError("Hole in ballot")
                    except MultiValueDictKeyError:
                        ballot_dict[pri] = None
                    except HoleInBallotError:
                        messages.warning(
                            request, "Ikke tillatt med hull i stemmeseddelen"
                        )
                        return redirect("voting-vote", pk=voting_id)
                ballot_dict = {
                    pri: v for pri, v in ballot_dict.items() if v is not None
                }
                voting.submit_stv_votes(request.user, ballot_dict)
            except UserAlreadyVoted:
                messages.error(request, "Du har allerede stemt i denne avstemningen!")
            except VotingDeactive:
                messages.error(
                    request, "Denne avstemningen er ikke lenger åpen for stemming!"
                )
            except DuplicatePriorities:
                messages.warning(
                    request, "Du kan ikke velge samme kandidat flere ganger!"
                )
                return redirect("voting-vote", pk=voting_id)
            else:
                messages.success(
                    request, f"Suksess! Du har stemt i avstemningen {voting.title}"
                )
        else:
            # Normal voting, first past the post(?)
            try:
                alternative = voting.alternatives.get(pk=request.POST["alternative"])
                alternative.add_vote(request.user)
            except (KeyError, Alternative.DoesNotExist):
                messages.warning(request, "Du har ikke valgt et alternativ.")
                return redirect("voting-vote", pk=voting_id)
            except UserAlreadyVoted:
                messages.error(request, "Du har allerede stemt i denne avstemningen!")
            except UserNotCheckedIn:
                messages.error(request, "Du har ikke sjekket inn!")
            except VotingDeactive:
                messages.error(
                    request, "Denne avstemningen er ikke lenger åpen for stemming!"
                )
            else:
                messages.success(
                    request, f"Suksess! Du har stemt i avstemningen {voting.title}"
                )
        return redirect("active-voting-list")

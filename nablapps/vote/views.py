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

from markdown_deux import markdown

from nablapps.accounts.models import NablaUser

from .forms import AlternativeFormset
from .models import (
    Alternative,
    BallotContainer,
    BallotEntry,
    DuplicatePriorities,
    HoleInBallotError,
    UnableToSelectWinners,
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


# @method_decorator(csrf_exempt, name="dispatch")  # TODO: Remove this, for tesing only
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
        "votes": alternative.get_num_votes(),
        "percentage": alternative.get_vote_percentage(),
    }


def _voting_serializer(voting, include_alternatives=True):
    response = {
        "pk": voting.pk,
        "title": voting.title,
        "active": voting.is_active,
        "num_voted": voting.get_total_votes(),
        "is_preference_vote": voting.is_preference_vote,
        "winners_pk": list(voting.winners.values_list("pk", flat=True)),
        "quota": voting.get_quota() if voting.is_preference_vote else None,
        "num_winners": voting.num_winners,
        "url": reverse("voting-edit", kwargs={"pk": voting.pk}),
        # If created_by is empty, assume it was created through admin
        # interface, and thus we do not know who made it.
        "created_by": getattr(voting.created_by, "username", "Admin (aka unknown)"),
        "description": markdown(voting.description),
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
        action = data.get("action")
        attendance_response = None
        if action == "check_out_all":
            self.object.check_out_all()
            attendance_response = _attendance_response()
        else:
            # TODO: exception handling
            identifier = data.get("identifier")
            attendance_response = register_attendance_any_identifier(
                self.object, identifier, action
            )
        users = self.object.checked_in_users.all()

        return JsonResponse(
            {
                "users": [_user_serializer(user) for user in users],
                "lastAction": attendance_response,
            }
        )


class VoteEventAPIView(VoteAdminMixin, BaseDetailView):
    """API view for getting information about voting event"""

    model = VotingEvent

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            eligible_group = self.object.eligible_group.name
        except AttributeError:  # eligible_group is None
            eligible_group = None
        return JsonResponse(
            {
                "title": self.object.title,
                "eligible_group": eligible_group,
                "num_checked_in": self.object.num_checked_in(),
                "users_should_poll": self.object.users_should_poll,
            }
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = json.loads(request.body)
        should_poll = data.get("users_should_poll")
        self.object.users_should_poll = should_poll
        self.object.save()
        return self.get(request, *args, **kwargs)


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
        to_change.is_active = data.get("active", to_change.is_active)
        if data.get("distribute_preferences", False):
            if not to_change.is_preference_vote:
                return JsonResponse(
                    {
                        "error": "Cannot distribute preference votes for non-preference vote"
                    },
                    status=400,
                )
            try:
                to_change.get_multi_winner_result()
            except UnableToSelectWinners as e:
                return JsonResponse({"error": str(e)}, status=409)  # 409 Conflict
        to_change.save()
        return self.get(request, *args, **kwargs)


class RegisterAttendanceView(VoteAdminMixin, DetailView):
    model = VotingEvent
    template_name = "vote/register_attendance.html"


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

    template_name = "vote/voting_form.html"
    model = Voting
    fields = ["event", "title", "description", "num_winners", "is_preference_vote"]

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
        # Yes, could probably have modified form, but culd not be bothered
        if self.object.get_total_votes() != 0:
            messages.error(
                self.request,
                "OBS! Denne avstemningen har allerede blitt stemt på, endring ikke gyldig",
            )
            return self.form_invalid(form, **kwargs)

        context = self.get_context_data()
        alternatives = context["alternatives"]
        with transaction.atomic():
            self.object = form.save()
            if alternatives.is_valid():
                alternatives.instance = self.object
                alternatives.save()
        event_pk = self.object.event.pk
        return redirect("voting-list", pk=event_pk)


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
        "is_preference": voting.is_preference_vote,
        "num_winners": voting.num_winners,
        "description": (
            markdown(voting.description)
            if voting.event.display_description_users
            else None
        ),
    }
    if include_alternatives:
        response["alternatives"] = [
            _alternative_public_serializer(a) for a in voting.alternatives.all()
        ]
    return response


class VotingsPublicAPIView(LoginRequiredMixin, BaseDetailView):
    """API endpoint for votings with only 'public' information, i.e. not including number of votes etc.

    POST submit a vote
     {'alternative_pk': ...}

    Discussion:
     Could probably merge this with VotingsAPIView, and dynamically include/exclude data depending on permissions
     or something similar.
     However, I did not bother.
     Feel free to do so if you want.

    TODO:
     Several places there are exceptions we catch, and then simply raise straight away.
     This is done simply to remind us where we probably should add some error handling.
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
                "polling_period": self.object.polling_period,
            }
        )

    def _submit_single_vote(self, request, data):
        try:
            alternative_pk = data.get("alternative_pk")
            alternative = Alternative.objects.get(pk=alternative_pk)
        except KeyError as e:
            # Invlaid pk
            raise e
        except Alternative.DoesNotExist as e:
            raise e

        alternative.add_vote(request.user)

    def _submit_preference_vote(self, request, data):
        try:
            priorities = data.get("priority_order")
        except KeyError as e:
            # Invlaid pk
            raise e

        if None in priorities:
            raise TypeError
        ballot = {i + 1: priority for i, priority in enumerate(priorities)}
        self.voting.submit_stv_votes(self.request.user, ballot)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            self.voting = Voting.objects.get(pk=data.get("voting_pk"))
        except Voting.DoesNotExist as e:
            raise e

        try:
            if self.voting.is_preference_vote:
                self._submit_preference_vote(request, data)
            else:
                self._submit_single_vote(request, data)
        except (
            UserNotCheckedIn,
            UserAlreadyVoted,
            UserNotEligible,
            VotingDeactive,
        ) as e:
            return JsonResponse({"error": str(e)}, status=403)  # 403 FORBIDDEN
        except TypeError:  # Raised by preference vote if ballot invalid
            return JsonResponse({"error": "Do not include null priorities"}, status=400)
        return self.get(request, *args, **kwargs)


class VoteEventPublicAPIView(LoginRequiredMixin, BaseDetailView):
    """Public API view for getting information about voting event"""

    model = VotingEvent

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return JsonResponse(
            {
                "title": self.object.title,
                # Report always checked in for events without checkin
                "checked_in": not self.object.require_checkin
                or self.object.user_checked_in(request.user),
            }
        )


class VotingEventUserView(LoginRequiredMixin, DetailView):
    """Collection of all votings for a given voting event"""

    model = VotingEvent
    template_name = "vote/voting_event_user_view.html"


class VoteEventList(LoginRequiredMixin, ListView):
    """Display list of active vote events"""

    model = VotingEvent
    template_name = "vote/voting_event_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        admin_rights = ["vote.vote_admin", "vote.vote_inspector"]
        context["admin_rights"] = any(
            [self.request.user.has_perm(right) for right in admin_rights]
        )
        return context

    def get_queryset(self):
        all_user_events = VotingEvent.objects.filter(eligible_group=None)
        user_group_events = VotingEvent.objects.filter(
            eligible_group__in=self.request.user.groups.all()
        )
        return chain(all_user_events, user_group_events)


class AdminVoteEventList(VoteAdminMixin, VoteEventList):
    """Displays all vote events for admin"""

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["is_admin_view"] = True
        return context

    def get_queryset(self):
        return VotingEvent.objects.all()

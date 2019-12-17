import string
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models import Model

from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView

from ..models.place import PlaceGrid, PlaceAction, extract_action, get_pixel_data, time_of_last_action



class PlaceView(DetailView):
    """DetailView displaying the grid with a given pk"""
    model = PlaceGrid
    template_name = "interactive/place.html"
    context_object_name = "grid"

    def get_object(self):
        obj = super().get_object()
        if not obj.is_published:
            raise Http404
        else:
            return obj

class NewestPlaceView(PlaceView):
    """DetailView displaying the latest grid"""
    def get_object(self):
        try:
            newest_enabled_place = PlaceGrid.objects.filter(publish_date__lte=datetime.now()).latest("publish_date")
        except PlaceGrid.DoesNotExist:
            raise Http404
        else:
            return newest_enabled_place


def get_place_info(request, pk):
    grid = get_object_or_404(PlaceGrid, pk=pk)
    if not grid.is_published:
        raise Http404
    return JsonResponse(
            {
                "width": grid.width,
                "height": grid.height,
                "cooldown": grid.cooldown,
                "enabled": grid.enabled,
                "legal_colors": grid.legal_colors,
            }
    )


def get_place_grid(request, pk):
    grid = get_object_or_404(PlaceGrid, pk=pk)
    if not grid.is_published:
        raise Http404

    # Preload the foreignkey to latest_action and user to avoid additional database queries
    qs = grid.lines.prefetch_related("pixels", "pixels__latest_action", "pixels__latest_action__user")

    grid_values = [
                [get_pixel_data(pixel) for pixel in line.pixels.all()]
                for line in qs.all()
    ]
    return JsonResponse(
            {
                "grid": grid_values,
                "last_updated": grid.last_updated.timestamp()
            }
    )


def get_place_history(request, pk):
    grid = get_object_or_404(PlaceGrid, pk=pk)
    if not grid.is_published:
        raise Http404

    # Preload the foreignkey to user to avoid additional database queries
    qs = grid.actions.select_related("user")

    # Get entire history
    return JsonResponse(list(map(extract_action, qs.all())), safe=False)


def get_place_updates(request, pk):
    """
    Return a JsonResponse with keys:
    last_updated : utc unix timestamp for the last time the grid was updated
    updates: list of actions since the given timestamp
    """

    grid = get_object_or_404(PlaceGrid, pk=pk)
    if not grid.is_published:
        raise Http404

    # Get only the latest action, created after `last_updated` for each pixel.
    # This is used to incrementally update the grid for the client

    updates = []
    try:
        last_updated = float(request.GET.get("last_updated", 0))
    except (ValueError, TypeError):
        return HttpResponse(status=400)

    grid_timestamp = grid.last_updated.timestamp()
    if grid_timestamp > last_updated:
        # Grid has been updated
        for line in grid.lines.all():
            if line.last_updated.timestamp() > last_updated:
                # Line has been updated
                for pixel in line.pixels.all():
                    if pixel.last_updated.timestamp() > last_updated:
                        # Pixel has been updated
                        # Add the latest action to that pixel to updates
                        action = pixel.latest_action
                        if action is not None:
                            updates.append(extract_action(action))

    return JsonResponse(
            {
                "last_updated": grid_timestamp,
                "updates": updates
            }
    )


@login_required
def submit_place(request, pk):
    grid = get_object_or_404(PlaceGrid, pk=pk)
    if not grid.is_published:
        raise Http404
    if request.method == "GET":
        # Return the time when the user last submitted a pixel
        try:
            latest_action = request.user.actions.filter(grid=grid).latest("time")
        except PlaceAction.DoesNotExist:
            time = 0
        else:
            time = latest_action.time.timestamp()
    
        resp = HttpResponse(time, status=200)
        return resp
    elif request.method == "POST":
        # Validate a pixel submission from a user
        if not grid.enabled:
            return HttpResponse(
                    "Submissions closed for this grid",
                    status=403
            )

        now = datetime.now() # Assumes system time is in UTC
        next_allowed_place = time_of_last_action(request.user, grid).timestamp() + grid.cooldown
        if next_allowed_place > now.timestamp():
            return HttpResponse("Still on cooldown", status=400)

        # The necessary data exists
        try:
            x = request.POST["x"]
            y = request.POST["y"]
            color = request.POST["color"]
        except KeyError:
            return HttpResponse("Missing data", status=400)

        # x and y have correct types
        try:
            x, y = int(x), int(y)
        except (ValueError, TypeError):
            return HttpResponse("Invalid x or y", status=400)


        # x and y have valid values
        if not 0 <= x < grid.width:
            return HttpResponse("x out of range", status=400)

        if not 0 <= y < grid.height:
            return HttpResponse("y out of range", status=400)

        # color has a valid value
        # if len(color) != 6 or not all(map(lambda x: x in string.hexdigits, color)):
        if color not in grid.legal_colors:
            return HttpResponse("Invalid color", status=400)

        # Create the action
        action = PlaceAction.objects.create(
                user=request.user,
                grid=grid,
                time=now,
                x=x,
                y=y,
                color=color
        )

        # If the grid was not updated after this pixel was submitted
        # then update the grid.
        if now > grid.last_updated:
            grid.last_updated = now
            grid.save()
            
            line = grid.lines.get(y=y)
            line.last_updated = now
            line.save()

            pixel = line.pixels.get(x=x)
            pixel.last_updated = now
            pixel.color = color
            pixel.latest_action = action
            pixel.save()

        return HttpResponse(now.timestamp(), status=200)


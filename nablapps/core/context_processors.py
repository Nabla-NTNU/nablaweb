import os

from nablapps.interactive.models import ColorChoice


def get_primary_dir(request):
    """Adds the primary URL path to context.

    For example, if the user is visting http://nabla.no/batman/cakes,
    primary_dir would be "batman".

    """
    primary_dir = request.path.split("/")[1]
    if primary_dir:
        primary_dir_slashes = "/" + primary_dir + "/"
    else:
        primary_dir_slashes = "/"
    return {"primary_dir": primary_dir, "primary_dir_slashes": primary_dir_slashes}


def get_navbar_color(request):
    """Returns the color of the navbar, based on default color from color-picker"""
    if os.environ.get("USE_CUSTOM_COLOR", "False") == "True":
        color = ColorChoice.get_average_color()
    else:
        color = None

    return {"custom_color": color}

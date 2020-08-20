# Vote for color

import datetime

from django.core.validators import RegexValidator, re
from django.db import models

from nablapps.accounts.models import NablaUser

# Copied from django_extras
color_re = re.compile(
    r"(^#[a-f0-9]{3,6}$)"  # Hash style
    r"|(^rgb\s*\(\s*((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*,\s*){2}((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*)\))"  # rgb style
    r"|(^hsl\s*\(\s*(360|3[0-5][0-9]|[0-2]?[0-9]{1,2})\s*,\s*(100%|[0-9]{1,2}%)\s*,\s*(100%|[0-9]{1,2}%)\s*\)$)",  # hsl style
    re.IGNORECASE,
)
validate_color = RegexValidator(
    color_re, "Enter a valid color in CSS format.", "invalid"
)


class ColorChoice(models.Model):
    """A users choice for color"""

    user = models.ForeignKey(NablaUser, on_delete=models.CASCADE)
    color = models.CharField(validators=[validate_color], max_length=20)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s choice of color {self.color} at {self.time}"

    # Attempt at making more sophisticated algorithm
    # working in the hsv-system. Feel free to fix and
    # implement this solution in the future.
    #
    # def get_average_color():
    #     """Returns average color"""ppp
    #     colors = ColorChoice.objects.all()
    #     hues = []
    #     values = []
    #     saturations = []
    #     for color in colors.values_list('color', flat=True):
    #         # color has format #rrggbb
    #         try:
    #             color = color.lstrip('#')
    #             r, g, b = [int(color[i:i+2], 16)/255 for i in [0,2,4]]
    #             hue = colorsys.rgb_to_hsv(r,g,b)[0]
    #             value = max([r,g,b])
    #             C = value - min([r,g,b])
    #             saturation = C/value if value > 0 else 0
    #             hues.append(hue)
    #             values.append(value)
    #             saturations.append(saturation)
    #         except:
    #             pass  # Ignore invalid colors
    #     hue = sum(hues) / len(hues)
    #     saturation = sum(saturations) / len(saturations)
    #     value = sum(values) / len(values)

    #     rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    #     return "#" + ''.join([hex(int(value*255))[-2:] for value in rgb])

    def get_average_color():
        time_limit = datetime.datetime.now() + datetime.timedelta(minutes=-20)
        colors = ColorChoice.objects.filter(time__gte=time_limit)
        reds = []
        greens = []
        blues = []
        for color in colors.values_list("color", flat=True):
            try:
                color = color.lstrip("#")
                r, g, b = [int(color[i : i + 2], 16) for i in [0, 2, 4]]
                reds.append(r)
                greens.append(g)
                blues.append(b)
            except:  # noqa: E722
                pass  # Ignore invalid colors
        if len(reds) == 0:
            return "#000000"

        r = sum(reds) / len(reds)
        g = sum(greens) / len(greens)
        b = sum(blues) / len(blues)
        return "#" + "".join([hex(int(value))[2:].zfill(2) for value in [r, g, b]])

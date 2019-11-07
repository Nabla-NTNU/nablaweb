# Vote for color

from django.db import models
from nablapps.accounts.models import NablaUser
from django.core.validators import re, RegexValidator

# Copied from django_extras
color_re = re.compile(
    r'(^#[a-f0-9]{3,6}$)'  # Hash style
    r'|(^rgb\s*\(\s*((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*,\s*){2}((2[0-4][0-9]|25[0-5]|1?[0-9]{1,2}|100%|[0-9]{1,2}%)\s*)\))'  # rgb style
    r'|(^hsl\s*\(\s*(360|3[0-5][0-9]|[0-2]?[0-9]{1,2})\s*,\s*(100%|[0-9]{1,2}%)\s*,\s*(100%|[0-9]{1,2}%)\s*\)$)',  # hsl style
    re.IGNORECASE
)
validate_color = RegexValidator(color_re, 'Enter a valid color in CSS format.', 'invalid')


class ColorChoice(models.Model):
    """A users choice for color"""

    user = models.ForeignKey(NablaUser, on_delete=models.CASCADE)
    color = models.CharField(validators=[validate_color], max_length=20)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s choice of color {self.color} at {self.time}"

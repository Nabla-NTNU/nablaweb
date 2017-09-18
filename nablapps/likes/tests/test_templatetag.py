from .base import BaseLikeTest

from django.template.base import Template
from django.template import Context


class TestTemplateTag(BaseLikeTest):
    def test_tag(self):
        t = Template(
"""
{% load like %}
{% show_like_button_for object %}
""")
        s = t.render(Context({"object": self.object, "user": self.user}))


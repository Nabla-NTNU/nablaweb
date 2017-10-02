from django.views.generic import ListView

from .models import DummyModel


class DummyList(ListView):
    model = DummyModel

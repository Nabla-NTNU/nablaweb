from django.views.generic import ListView

from nablapps.interactive.models.games import Game


class GamesList(ListView):
    """List of games"""

    model = Game
    context_object_name = "games_list"
    template_name = "games_list.html"
    paginate_by = 8
    queryset = Game.objects.all()

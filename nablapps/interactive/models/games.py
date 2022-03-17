# Models for game_list
from django import template
from django.db import models

register = template.Library()


class Game(models.Model):
    class Meta:
        ordering = ["index"]

    index = models.IntegerField(help_text="Bruk helst 10, 20, 30 osv.")
    title = models.TextField()
    url = models.TextField(
        help_text="Denne lenken må være relativ ettersom den settes sammen med url-en vår. Altså: hvis man vil lenke til https://nabla.no/kodegolf/ må man skrive inn 'kodegolf/' (uten fnutter). (Ikke hele lenken, da får man: https://nabla.no/https://nabla.no/kodegolf/, som ikke fungerer.)"
    )
    picture = models.ImageField(
        upload_to="uploads/game_pictures",
        null=True,
        blank=True,
        verbose_name="Bilde",
        help_text="Bruk samme størrelse på alle bilder, helst 770x300 px",
    )

    def __str__(self):
        return self.title

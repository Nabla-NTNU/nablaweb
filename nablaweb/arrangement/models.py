from django.db import models
from django.contrib.auth.models import User

# Dummy-klasse
class Nyhet(models.Model):
    """class Nyhet(models.Model)"""

    tittel = models.CharField(max_length=100)
    ingress = models.TextField()
    brodtekst = models.TextField()


class Arrangement(Nyhet):
    """class Arrangement(Nyhet)"""

    class Meta:
        verbose_name_plural = "arrangement"

    sted = models.CharField(max_length=100)
    tid = models.DateTimeField()

    aapen = models.BooleanField(default=False)
    plasser = models.PositiveIntegerField(default=0)
    paameldte = models.ManyToManyField(User)

    paameldingsfrist = models.BooleanField(default=False)
    frist = models.DateTimeField()

    ikke_fysmat = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s, %s" % (self.tittel[:20], self.tid.strftime("%d/%m/%y"))

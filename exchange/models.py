from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.contrib.flatpages.models import FlatPage


class University(models.Model):
    univ_navn = models.CharField(
        max_length=50,
        verbose_name='universitets navn',
        blank=False,
        help_text='Navnet til universitetet',
        default="",
    )

    class Meta:
        ordering = ['univ_navn']

    land = models.CharField(
        max_length=30,
        verbose_name='land',
        blank=False,
        help_text='Landet universitetet ligger i',
        default="",
    )

    def __str__(self):
        return self.univ_navn

RETNINGER = (
    ("Biofysikk og medisinteknologi", "biofys"),
    ("Industriell matematikk", "indmat"),
    ("Teknisk fysikk", "tekfys")
)


class Exchange(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['student']

    retning = models.CharField(
        max_length=30,
        blank=False,
        help_text='Retning',
        choices=RETNINGER,
    )

    start = models.DateField(
        blank=False,
        help_text='Dato utveksling startet'
    )
    end = models.DateField(
        blank=False,
        help_text='Dato utveksling sluttet'
    )
    univ = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student) + ' - ' + str(self.univ)


class Info(FlatPage):
    ex = models.ForeignKey(Exchange, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.url = '/utveksling/' +str(self.ex.univ.pk) + '/' + self.title.replace(" ", "-") + '/'
        super(Info, self).save()


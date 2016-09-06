from django.db import models
from django.conf import settings


class University(models.Model):
    univ_navn = models.CharField(
        max_length=50,
        verbose_name='universitets navn',
        blank=False,
        help_text='Navnet til universitetet',
        default="",
    )

    desc = models.TextField(
        verbose_name="beskrivelse",
        blank=True,
        help_text="En kort beskrivelse av universitetet. Valgfritt."
    )

    land = models.CharField(
        max_length=30,
        verbose_name='land',
        blank=False,
        help_text='Landet universitetet ligger i',
        default="",
    )

    class Meta:
        verbose_name = "universitet"
        verbose_name_plural = "universiteter"
        ordering = ['univ_navn']

    def __str__(self):
        return self.univ_navn

    def get_has_retning_list(self):
        """ Returns a list of booleans indicating whether there exists an exchange in each retning"""
        return [
            self.exchange_set.filter(retning=retn).exists()
            for retn, _ in RETNINGER
        ]


RETNINGER = (
    ("biofys", "Biofysikk og medisinteknologi"),
    ("indmat", "Industriell matematikk"),
    ("tekfys", "Teknisk fysikk")
)


class Exchange(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    univ = models.ForeignKey(University, on_delete=models.CASCADE)

    retning = models.CharField(
        max_length=6,
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

    class Meta:
        verbose_name = "utveksling",
        verbose_name_plural = "utvekslinger"
        ordering = ['student']

    def __str__(self):
        return str(self.student) + ' - ' + str(self.univ)


class Info(models.Model):
    ex = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    title = models.CharField(
        verbose_name="tittel",
        max_length=50,
        blank=False,
        help_text="Tittelen til innholdet",
        default="",
    )
    body = models.TextField(
        verbose_name="brødtekst",
        blank=True,
        help_text=(
            "Man kan her bruke <a href=\"http://en.wikipedia.org/wiki/Markdown\" target=\"_blank\">"
            "markdown</a> for å formatere teksten."))

    class Meta:
        verbose_name = "info",
        verbose_name_plural = "info"

    def __str__(self):
        return self.title

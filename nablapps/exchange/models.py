from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from nablapps.news.models import AbstractNewsArticle


class University(models.Model):
    univ_navn = models.CharField(
        max_length=50,
        verbose_name="universitets navn",
        blank=False,
        help_text="Navnet til universitetet",
        default="",
    )

    desc = models.TextField(
        verbose_name="beskrivelse",
        blank=True,
        help_text="En kort beskrivelse av universitetet. Valgfritt.",
    )

    land = models.CharField(
        max_length=30,
        verbose_name="land",
        blank=False,
        help_text="Landet universitetet ligger i",
        default="",
    )

    by = models.CharField(
        max_length=30,
        verbose_name="by",
        blank=False,
        help_text="Byen universitetet ligger i",
        default="",
    )

    class Meta:
        verbose_name = "universitet"
        verbose_name_plural = "universiteter"
        ordering = ["univ_navn"]

    def __str__(self):
        return self.univ_navn

    def get_has_retning_list(self):
        """Return a list of booleans indicating whether there exists an exchange in each retning"""
        return [
            self.exchange_set.filter(retning=retn).exists() for retn, _ in RETNINGER
        ]


RETNINGER = (
    ("biofys", "Biofysikk og medisinteknologi"),
    ("indmat", "Industriell matematikk"),
    ("tekfys", "Teknisk fysikk"),
)


class Exchange(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    univ = models.ForeignKey(University, on_delete=models.CASCADE)

    retning = models.CharField(
        max_length=6,
        blank=False,
        help_text="Retning",
        choices=RETNINGER,
    )

    start = models.DateField(
        blank=False, help_text="Dato utveksling startet. Kun måned som brukes."
    )
    end = models.DateField(
        blank=False, help_text="Dato utveksling sluttet. Kun måned som brukes."
    )

    fag = models.TextField(blank=True, null=True, help_text="Fag du tok.")
    annet = models.TextField(blank=True, null=True, help_text="Annet.")
    facebook = models.CharField(blank=True, null=True, max_length=100, help_text="Link til din facebookprofil (valgfritt).")

    class Meta:
        verbose_name = "utveksling"
        verbose_name_plural = "utvekslinger"
        ordering = ["student"]

    def __str__(self):
        return f"{self.student} - {self.univ}"


def validate_file_extension(value):
    if not value.name.endswith(".pdf"):
        raise ValidationError("Må være en PDF-fil")


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
            'Man kan her bruke <a href="http://en.wikipedia.org/wiki/Markdown" target="_blank">'
            "markdown</a> for å formatere teksten."
        ),
    )

    file = models.FileField(
        upload_to="utveksling",
        verbose_name="PDF-fil",
        blank=True,
        null=True,
        help_text="PDF-fil. Hvis dette eksisterer vil ikke teksten ovenfor bli brukt.",
        validators=[validate_file_extension],
    )

    link = models.TextField(
        verbose_name="ekstern link",
        blank=True,
        help_text="Link som kan brukes i stedet for pdf-fil eller tekst. Har høyest prioritet",
    )

    class Meta:
        verbose_name = "info"
        verbose_name_plural = "info"

    def __str__(self):
        return self.title


class ExchangeNewsArticle(AbstractNewsArticle):
    def get_absolute_url(self):
        """Get the url of the news-article"""
        return reverse("ex_news_detail", kwargs={"pk": self.pk, "slug": self.slug})

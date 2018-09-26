"""
Models for jobs app

Defines mainly the Advert and Company models.
"""
from datetime import datetime
from django.urls import reverse
from django.db import models
from content.models import WithPicture, TimeStamped
from nablapps.news.models import TextContent


# Det er litt stygt å bruke modeller for YearChoices og RelevantForChoices, men
# det var den enkle måten å få riktige forms i admin på.


class YearChoices(models.Model):
    """
    Model for each choice for study year in adverts.
    This should really not be a model, because this is static content.
    """
    year = models.IntegerField(
        blank=False,
        verbose_name="Klasse",
        help_text="Klasse: 1, 2, 3, 4 og 5"
    )

    class Meta:
        verbose_name = "Klasse"
        verbose_name_plural = "Klasser"
        permissions = (
            ("can_see_static_models", "Can see static models"),
        )

    def __str__(self):
        return f'{self.year}. klasse'


class RelevantForChoices(models.Model):
    """
    Model for choices for who an advert is relevant for.
    """
    studieretning = models.CharField(
        max_length=50,
        verbose_name="Valg",
        help_text='Mulige valg for "relevant for" når man legger til stillingsannonser.')

    class Meta:
        verbose_name = 'Mulig valg for "relevant for"'
        verbose_name_plural = 'Mulige valg for "relevant for"'

    def __str__(self):
        return self.studieretning


class TagChoices(models.Model):
    """Tags for adverts"""
    tag = models.CharField(
        max_length=100,
        verbose_name="Tags",
        help_text=("Tags for stillingsannonsen. "
                   "Eksempler: deltid, sommerjobb, fulltid, utlandet, by. Søkbar."),
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ("tag",)

    def __str__(self):
        return self.tag


class Company(WithPicture):
    """
    Model representing a company which has an advert out for a job.
    """
    website = models.URLField(max_length=200, blank=True, verbose_name="Nettside")
    name = models.CharField(verbose_name="navn", max_length=200, blank=False)
    description = models.TextField(verbose_name="beskrivelse", blank=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name = "bedrift"
        verbose_name_plural = "bedrifter"
        ordering = ("name",)

    def __str__(self):
        return self.name


class AdvertManager(models.Manager):
    """Model manager for Advert model"""
    def active(self):
        """Get only active adverts"""
        return self.exclude(removal_date__lte=datetime.now())


class Advert(TimeStamped, TextContent):
    """
    Model representing an advert for a job.
    """
    company = models.ForeignKey(
        'Company',
        verbose_name="Bedrift",
        on_delete=models.CASCADE,
        help_text="Hvilken bedrift stillingen er hos")

    relevant_for_group = models.ManyToManyField(
        RelevantForChoices,
        blank=False,
        verbose_name="Studieretning",
        help_text="Hvilke studieretninger stillingsannonsen er relevant for.")
    relevant_for_year = models.ManyToManyField(
        YearChoices,
        blank=False,
        verbose_name="Årskull",
        help_text="Hvilke årskull stillingsannonsen er relevant for.")
    tags = models.ManyToManyField(
        TagChoices,
        blank=True,
        verbose_name="Tags",
        help_text="F.eks. sommerjobb, bergen, kirkenes, olje, konsultering...")

    deadline_date = models.DateTimeField(
        verbose_name="Frist",
        blank=True,
        null=True,
        help_text="Søknadsfrist")

    removal_date = models.DateTimeField(
        verbose_name="Forsvinner",
        blank=False,
        help_text="Når annonsen fjernes fra listen, f.eks. samtidig som søknadsfristen")

    info_file = models.FileField(
        upload_to="stillinger",
        blank=True,
        verbose_name="Informasjonsfil",
        help_text="Informasjon om stillingen")
    info_website = models.URLField(
        blank=True,
        max_length=150,
        verbose_name="Infoside",
        help_text="Nettside der man kan søke på stillingen eller få mer informasjon")

    class Meta:
        ordering = ("-created_date", "headline")
        verbose_name = "stillingsannonse"
        verbose_name_plural = "stillingsannonser"

    objects = AdvertManager()

    def __str__(self):
        return self.headline

    @property
    def picture(self):
        """
        Get picture for the advert
        This is here mostly for making adverts compatible with the front page.
        """
        return self.company.picture

    @property
    def cropping(self):
        """
        Get cropping corresponding to the picture.
        This is here mostly for making adverts compatible with the front page.
        """
        return self.company.cropping

    def get_absolute_url(self):
        """Get the canonical url for the advert."""
        return reverse("advert_detail", kwargs={'pk': self.pk, 'slug': self.slug})

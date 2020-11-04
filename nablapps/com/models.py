"""
Modeller for com-appen
"""

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField


class ComPage(models.Model):
    """Model til en komiteside"""

    com = models.ForeignKey(Group, on_delete=models.CASCADE)

    picture = models.ImageField(
        upload_to="uploads/com_pictures",
        null=True,
        blank=True,
        verbose_name="Bilde",
        help_text=("Last opp din undergruppes logo."),
    )

    is_interest_group = models.BooleanField(
        verbose_name="Interessegruppe",
        help_text="Er ikke fullverdig komité",
        default=True,
    )

    description = RichTextField(
        config_name="basic",
        verbose_name="Beskrivelse", help_text="Teksten på komitésiden", blank=True
    )

    slug = models.CharField(
        verbose_name="Slug til URL-er",
        max_length=50,
        blank=False,
        unique=True,
        editable=False,
    )

    last_changed_date = models.DateTimeField(
        verbose_name="Sist redigert", auto_now=True, null=True
    )

    last_changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Sist endret av",
        related_name="%(class)s_edited",
        editable=False,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "komiteside"
        verbose_name_plural = "komitesider"

    def __str__(self):
        return self.com.name

    def has_been_edited(self):
        return self.last_changed_by is not None

    def get_canonical_name(self):
        return slugify(str(self))

    def get_absolute_url(self):
        return reverse("show_com_page", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = self.get_canonical_name()
        super().save(*args, **kwargs)

    def get_picture_url(self):
        """Return the absolute url of the main picture"""
        domain = Site.objects.get_current().domain  # noqa: F821
        media_url = settings.MEDIA_URL
        filename = self.picture.name
        return f"http://{domain}{media_url}{filename}"


class ComMembership(models.Model):
    """Komitemedlemskap (many to many)"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    com = models.ForeignKey(
        "auth.Group", verbose_name="Komité", on_delete=models.CASCADE
    )
    story = models.TextField(
        blank=True, verbose_name="Beskrivelse", help_text="Ansvarsområde eller lignende"
    )
    joined_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Ble med",
        help_text="Dato personen ble med i komiteen",
    )
    is_active = models.BooleanField(
        blank=False, null=False, verbose_name="Aktiv?", default=True
    )

    class Meta:
        verbose_name = "komitemedlem"
        verbose_name_plural = "komitemedlemmer"

    def save(self, *args, **kwargs):
        self.com.user_set.add(self.user)
        self.user.is_staff = True
        self.user.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.com.user_set.remove(self.user)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Committee(models.Model):
    """
    Representerer en komite
    """

    group = models.OneToOneField(
        to="auth.Group",
        primary_key=True,
        on_delete=models.CASCADE,
        verbose_name="Gruppe",
    )

    page = models.OneToOneField(
        to="com.ComPage",
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Komitéside",
    )

    mail_list = models.EmailField(verbose_name="Epostliste", blank=True)

    name = models.CharField(_("name"), max_length=80, unique=True)

    leader = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name="Leder",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Komité"
        verbose_name_plural = "Komitéer"

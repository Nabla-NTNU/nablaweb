"""
Models for album app
"""
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension
from django.db import models
from django.forms import ClearableFileInput, FileField, ModelChoiceField, ModelForm
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey

from nablapps.core.models import BaseImageModel, TimeStamped


class AlbumImage(BaseImageModel):
    """
    An album image.

    Each album image is associated with a single album
    """

    description = models.TextField(verbose_name="Bildetekst", blank=True, null=True)

    album = models.ForeignKey(
        "album.Album",
        verbose_name="Album",
        related_name="images",
        null=True,
        on_delete=models.CASCADE,
    )

    num = models.PositiveIntegerField(
        verbose_name="Nummer", blank=True, null=True, editable=False
    )

    is_display_image = models.BooleanField(
        verbose_name="Er visningbilde",
        help_text="Bildet som vises i listen over album",
        default=False,
    )

    def get_absolute_url(self):
        """Get canonical url for image"""
        return reverse("album_image", kwargs={"pk": self.album.id, "num": self.num + 1})

    @property
    def is_published(self):
        """Check is parent album is hidden (meaning unpublished)"""
        return self.album.visibility != "h"

    class Meta:
        verbose_name = "Albumbilde"
        verbose_name_plural = "Albumbilder"
        db_table = "content_albumimage"


class Album(MPTTModel, TimeStamped):
    """
    Model representing an album which is a collection of images.
    """

    title = models.CharField(
        max_length=100, verbose_name="Albumtittel", blank=False, null=True
    )

    VISIBILITY_OPTIONS = (("p", "public"), ("u", "users"), ("h", "hidden"))

    visibility = models.CharField(
        max_length=1,
        verbose_name="Synlighet",
        choices=VISIBILITY_OPTIONS,
        default="h",
        blank=False,
    )

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Forelder",
        help_text="Bildealbum som dette albumet hører til. Album er relaterte med en trestruktur.",
    )

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Album"
        db_table = "content_album"

    def get_absolute_url(self):
        """Return canonical url for album"""
        return reverse("album", kwargs={"pk": self.pk})

    def is_visible(self, user=AnonymousUser()):
        """
        Return whether this album is visible for the supplied user.

        If visibility is 'p' then all users can see the album.
        If visibility is 'u' all logged in users can see the album.
        All logged in users with the permission to change albums can see the album.
        """
        return (
            self.visibility == "p"
            or self.visibility == "u"
            and user.is_authenticated
            or user.has_perm("content.change_album")
        )

    @property
    def first(self):
        """Get the image which is considered to be the first in the album"""
        return self.images.order_by("-is_display_image", "num").first()

    def __str__(self):
        return self.title


class AlbumForm(ModelForm):
    # model = Album
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].queryset = Album.objects.exclude(
            pk__in=self.instance.get_descendants(include_self=True)
        )

    class Meta:
        model = Album
        fields = ("title", "visibility", "parent")

    parent = ModelChoiceField(
        Album.objects.all(),
        required=False,
        label="Forelder",
        help_text="Bildealbum som dette albumet hører til. (Album er relaterte med en trestruktur.)",
    )
    photos = FileField(
        widget=ClearableFileInput(attrs={"multiple": True}),
        label="Legg til flere bilder",
        help_text="Last opp flere bilder her. Når du lagrer dukker de opp i oversikten under",
        required=False,
    )

    # def clean_parent(self):
    #     super()
    def clean_parent(self):
        parent_obj = self.cleaned_data["parent"]
        current_obj = self.instance
        print(current_obj.get_children())
        if parent_obj == current_obj:
            raise ValidationError("Et album kan ikke være sin egen forelder")
        elif parent_obj in current_obj.get_descendants(include_self=True):
            raise ValidationError(
                "En node kan ikke være barn av noen av sine etterkommere."
            )
        return parent_obj

    def clean_photos(self):
        """Make sure only images can be uploaded."""
        for upload in self.files.getlist("photos"):
            validate_image_file_extension(upload)

    def save_photos(self, album):
        """Process each uploaded image."""
        for file in self.files.getlist("photos"):
            photo = AlbumImage(album=album, file=file)
            photo.save()

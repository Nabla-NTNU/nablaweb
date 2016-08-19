from django.core.urlresolvers import reverse
from django.db import models

class Universitet(models.Model):
    univ_navn = models.CharField(
        max_length=30,
        verbose_name='universitets navn',
        blank=False,
        null=True,
        help_text='Universitets navn',
        default = "",
    )
    class Meta:
        ordering=("univ_navn",)

    land = models.TextField(
        verbose_name='land',
        blank=False,
        null=True,
        help_text='Land',
        default = "",
    )

    def get_absolute_url(self):
        return reverse("exchange:ex_detail_list", kwargs={"id": self.id})
        # return  "/posts/%s/" %(self.id)


    def __str__(self):
        return self.univ_navn

RETNINGER = (
    ("Biofysikk og medisinteknologi","Biofysikk og medisinteknologi"),
    ("Industriell matematikk","Industriell matematikk"),
    ("Teknisk fysikk","Teknisk fysikk")
)
CHOICES = Universitet.objects.values_list('univ_navn','univ_navn')


class Utveksling(models.Model):
    student_navn = models.CharField(
        max_length=30,
        verbose_name='student_navn',
        blank=False,
        null=True,
        help_text='Student navn'
    )
    class Meta:
        ordering=("student_navn",)

    retning = models.CharField(
        max_length=30,
        blank=False,
        null = True,
        help_text='Retning',
        choices = RETNINGER,
    )
    epost = models.CharField(
        max_length=50,
        null=True,
        help_text='E-post',
        default="",
    )


    ex_year = models.IntegerField(
        verbose_name = "Arstall",
        blank=False,
        null=True,
    )
    univ_navn = models.CharField(
        max_length=30,
        blank=False,
        choices=CHOICES,
        null=True,

    )



    def __str__(self):
        return self.student_navn

class Link(models.Model):
    link_info = models.CharField(
        max_length=120,
        verbose_name='link info',
        blank=False,
        null=True,
        help_text='Link info'
    )
    class Meta:
        ordering=("link_info",)

    linken = models.TextField(
        verbose_name='linken',
        blank=False,
        null=True,
        help_text='Linken'
    )
    univ_navn = models.CharField(
        verbose_name='Universitet',
        max_length=30,
        blank=False,
        choices=CHOICES,
        null=True,

    )

    def __str__(self):
        return self.link_info

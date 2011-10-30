from django.db import models
from content.models import Content

# Create your models here.

class Nablad(Content):
    pub_date = models.DateField(verbose_name='publisert',  blank=True, null=True)
    file = models.FileField(upload_to='nabladet', verbose_name='PDF-fil')

    class Meta:
        verbose_name = 'et nablad'
        verbose_name_plural = 'nablad'

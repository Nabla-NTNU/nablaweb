from django.db import models

class Reklame(models.Model):
    advertiser = models.CharField(verbose_name="reklamør", max_length=200, blank=False)
    link = models.CharField(verbose_name="lenke", max_length=200, blank=False)
    image = models.ImageField(max_length=4096, blank=False)
    
    def __unicode__(self):
        retstring = self.advertiser + "_" + self.id
        return retstring

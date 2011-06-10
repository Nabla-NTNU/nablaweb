from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    telephone = models.CharField("Telefon", max_length = 15, blank=True)
    cell_phone = models.CharField("Mobil", max_length = 15, blank=True)
    birthday = models.DateField("Bursdag", blank =True, null=True)
    address = models.CharField("Adresse", max_length = 40, blank = True)
    mail_number = models.CharField("Postnr", max_length = 4, blank = True)
    web_page = models.CharField("Hjemmeside", max_length = 80, blank = True)
    wants_email = models.BooleanField("Motta kullmail", default = True)
    about = models.TextField("Biografi",blank = True)
    ntnu_card_number = models.CharField("NTNU kortnr",max_length = 20, blank = True)

    def __unicode__(self):
        return "< %s profile >" % self.user.username

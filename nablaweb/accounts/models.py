from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    telephone = models.CharField(max_length = 15, blank=True)
    cell_phone = models.CharField(max_length = 15, blank=True)
    birthday = models.DateField(blank =True, null=True)
    address = models.CharField(max_length = 40, blank = True)
    mail_number = models.CharField(max_length = 4, blank = True)
    web_page = models.CharField(max_length = 80, blank = True)
    wants_email = models.BooleanField(default = True)
    about = models.TextField(blank = True)
    ntnu_card_number = models.CharField(max_length = 20, blank = True)

    def __unicode__(self):
        return "< %s profile >" % self.user.username

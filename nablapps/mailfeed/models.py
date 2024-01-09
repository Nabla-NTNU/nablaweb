from django.db import models


class MailFeed(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False)
    created = models.DateTimeField(auto_now=True, verbose_name="Opprettet")

    def get_email_list(self):
        subscription_list = Subscription.objects.filter(mailfeed=self)
        email_list = [sub.email for sub in subscription_list]
        return email_list


class Subscription(models.Model):
    mailfeed = models.ForeignKey(MailFeed, on_delete=models.CASCADE)
    email = models.EmailField(blank=False, null=False)
    created = models.DateTimeField(auto_now=True, verbose_name="Opprettet")

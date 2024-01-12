from uuid import uuid4

from django.db import models


class Mailfeed(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False)
    created = models.DateTimeField(auto_now=True, verbose_name="Opprettet")

    def get_email_list(self) -> list[str]:
        subscription_list = Subscription.objects.filter(mailfeed=self)
        email_list = [sub.email for sub in subscription_list]
        return email_list

    class Meta:
        permissions = [
            ("generate_mailfeeds", "can generate mailfeeds"),
        ]

    def __str__(self) -> str:
        return self.name


class Subscription(models.Model):
    mailfeed = models.ForeignKey(Mailfeed, on_delete=models.CASCADE)
    email = models.EmailField(blank=False, null=False)
    uuid = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now=True, verbose_name="Opprettet")

    def save(self, *args, **kwargs):
        self.uuid = uuid4()
        super(Subscription, self).save(*args, **kwargs)

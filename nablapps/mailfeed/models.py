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


class Subscription(models.Model):
    mailfeed = models.ForeignKey(Mailfeed, on_delete=models.CASCADE)
    email = models.EmailField(blank=False, null=False)
    created = models.DateTimeField(auto_now=True, verbose_name="Opprettet")

from django.conf import settings
from django.db import models


class Committee(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    def get_mailinglist(self):
        """Returns the mailinglist to the
        applicants to the committee for this application_round"""
        return ";".join(
            [
                application.applicant.email
                for application in Application.objects.filter(
                    committee=self
                ).prefetch_related("applicant")
            ]
        )


class ApplicationRound(models.Model):
    """An application round, ie. fall"""

    name = models.CharField(
        max_length=20, help_text="Navn på opptaksrunde, f.eks. vår 2022"
    )
    is_active = models.BooleanField(
        default=False,
        help_text="Er aktiv nå. Kun en opptaksrunde kan være aktiv om gangen.",
    )

    def get_applicants(self):
        return Application.objects.filter(application_round=self)

    def __str__(self):
        state = "active" if self.is_active else "inactive"
        return f"ApplicationRound {self.name}, {state}"

    def get_current():
        """Returns the current ApplicationRound, ie. is_active is True
        Returns empty if no active ApplicationRound"""
        try:
            return ApplicationRound.objects.get(is_active=True)
        except ApplicationRound.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        # Only one application round should be active at
        # any given time.
        if self.is_active:
            # Deactivate all others
            ApplicationRound.objects.filter(is_active=True).exclude(pk=self.pk).update(
                is_active=False
            )
        super().save(*args, **kwargs)


class Application(models.Model):
    application_round = models.ForeignKey(to=ApplicationRound, on_delete=models.CASCADE)
    applicant = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    committee = models.ForeignKey(to=Committee, on_delete=models.CASCADE)
    priority = models.IntegerField()
    application_text = models.TextField(blank=True)
    anonymous = models.BooleanField(
        help_text="Bruker ønsker å være anonym på søkerlisten"
    )

    def __str__(self):
        return f"{self.applicant}'s application for {self.committee} in {self.application_round}"

    class Meta:
        unique_together = [
            # Only one of each priority per round
            ["application_round", "applicant", "priority"],
            # Can only search a committee once per round
            ["application_round", "applicant", "committee"],
        ]

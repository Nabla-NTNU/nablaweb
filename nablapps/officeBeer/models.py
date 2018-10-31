from django.db import models

class Account(models.Model):
    """
    A users balance in the office beer system
    """

    balance = models.IntegerField(
        'Balanse'
        )

    user = models.OneToOne(
        settings.AUTH_USER_MODEL,
        editable=False,
        on_delete=models.CASCADE
    )


class Transaction(models.Model):
    """
    Represents a transaction, either in or out
    """

    amount = models.IntegerField(
        'Penger'
        )

    account = models.ForeignKey(
        Account
        )

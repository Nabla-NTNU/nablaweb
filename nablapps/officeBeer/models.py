from django.db import models
from django.conf import settings

class Account(models.Model):
    """
    A users balance in the office beer system
    """

    balance = models.IntegerField(
        'Balanse',
        default=0
        )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        editable=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.get_full_name()}'s office beer account"
        
class Transaction(models.Model):
    """
    Represents a transaction, either in or out
    """

    description = models.CharField(
        'Forklaring av transaksjon',
        max_length = 30)
        
    amount = models.IntegerField(
        'Penger'
        )

    account = models.ForeignKey(
        Account
        )

    date = models.DateTimeField(
        'Dato'
        )

class Product(models.Model):
    """
    Products one can buy
    """
    name = models.CharField(
        'Navn på produkt',
        max_length = 30)
    price = models.IntegerField(
        'Pris'
        )

    def __str__(self):
        return self.name

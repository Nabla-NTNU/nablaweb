from django.db import models
from django.conf import settings
from django.utils.timezone import now

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
        'Dato',
        default = now
        )

    def __str__(self):
        return f"{self.account.user.get_full_name()} - {self.amount}kr"
        
    class Meta:
        permissions = (
            ("sell_product", "Can administer the purchase view"),
            )

class DepositRequest(models.Model):
    """
    Todo: write docstring
    """

    amount = models.IntegerField(
        'Beløp'
        )

    account = models.ForeignKey(
        Account
        )

    def approve(self):
        # Approve request and create a positive transaction
        self.account.balance += self.amount
        self.account.save()
        Transaction(description="Deposit", amount=self.amount, account=self.account).save()
        self.delete()

    def __str__(self):
        return f"{self.account.user.get_full_name()}'s deposit request of kr {self.amount}"
        
    
class Product(models.Model):
    """
    Products one can buy
    """
    name = models.CharField(
        'Navn på produkt',
        max_length = 30)
    price = models.PositiveIntegerField(
        'Pris'
        )

    def __str__(self):
        return self.name

from django.contrib import admin

from .models import Account, Product

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """
    Admin interface for Account model
    """

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for Product
    """
    

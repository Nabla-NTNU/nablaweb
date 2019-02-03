from django.contrib import admin

from .models import Account, Product, DepositRequest, Transaction

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
    
@admin.register(DepositRequest)
class DepositRequestAdmin(admin.ModelAdmin):
    """
    Admin interface for DepositRequest
    """
    def approve(self, request, queryset):
        for request in queryset:
            request.approve()

    actions = [approve]

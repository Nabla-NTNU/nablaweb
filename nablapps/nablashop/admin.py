from django.contrib import admin

from .models import Category, Order, OrderProduct, Product

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderProduct)
admin.site.register(Order)

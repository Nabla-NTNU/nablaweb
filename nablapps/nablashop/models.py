from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from django.shortcuts import reverse

from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(
        max_length=30, verbose_name="Kategorisk navn", default="Kategori"
    )
    description = RichTextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategorier"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Navn", default="Produkt")
    description_short = RichTextField()
    description = RichTextField(config_name="basic")
    pub_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(
        upload_to="product_photo", blank=False, verbose_name="bilde"
    )
    price = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="pris", default=0
    )
    stock = models.IntegerField(verbose_name="antall", default=0)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.CASCADE
    )
    slug = models.SlugField(default="test-product")

    def __str__(self):
        return self.name

    def get_add_to_cart_url(self):
        return reverse("nablashop:add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("nablashop:remove-from-cart", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkter"


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_final_price(self):
        return self.get_total_product_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        return total

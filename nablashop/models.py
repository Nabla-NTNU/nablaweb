from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='Kategorisk navn', default='Kategori')
    description = models.TextField(verbose_name='Beskrivelse', default='Her ligger masse rart')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategorier"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Navn', default='Produkt')
    description_short = models.TextField(verbose_name='Kort beskrivelse', default='Ting')
    description = models.TextField(verbose_name='Beskrivelse', default='Ting')
    pub_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='product_photo', blank=False, verbose_name='bilde')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='pris', default='123')
    category = models.ForeignKey(Category, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Produkt'
        verbose_name_plural = 'Produkter'


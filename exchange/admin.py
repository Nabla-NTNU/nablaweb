from django.contrib import admin
from .models import University, Exchange, Info


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ["student"]
    search_fields = ["student"]

    class Meta:
        model = Exchange


class UniversityAdmin(admin.ModelAdmin):
    list_display = ["univ_navn"]
    search_fields = ["univ_navn"]

    class Meta:
        model = University


class InfoAdmin(admin.ModelAdmin):
    exclude = ('url',)

    class Meta:
        model = Info

admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(Info, InfoAdmin)

# Register your models here.

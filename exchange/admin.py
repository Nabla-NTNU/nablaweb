from django.contrib import admin
from .models import University, Exchange, Info


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("get_full_name", "univ")

    def get_full_name(self, obj):
        return obj.student.get_full_name()

    get_full_name.short_description = "student"

    class Meta:
        model = Exchange


class UniversityAdmin(admin.ModelAdmin):
    list_display = ["univ_navn"]
    search_fields = ["univ_navn"]

    class Meta:
        model = University


class InfoAdmin(admin.ModelAdmin):
    list_display = ["title"]

    class Meta:
        model = Info

admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(Info, InfoAdmin)

# Register your models here.

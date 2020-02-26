from django.contrib import admin

from image_cropping import ImageCroppingMixin

from nablapps.core.admin import ChangedByMixin
from nablapps.news.admin import add_to_frontpage

from .models import Exchange, ExchangeNewsArticle, Info, University


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


class ExchangeNewsAdmin(ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    """Admin interface for NewsArticle"""

    prepopulated_fields = {"slug": ("headline",)}
    actions = [add_to_frontpage]


admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(ExchangeNewsArticle, ExchangeNewsAdmin)

# Register your models here.

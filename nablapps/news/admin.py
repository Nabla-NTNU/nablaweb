from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from image_cropping import ImageCroppingMixin
from content.admin import ChangedByMixin

from .models import News
from .forms import NewsForm


@admin.register(News)
class NewsAdmin(ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    form = NewsForm
    fields = ("publication_date",
              "published",
              "picture",
              "cropping",
              "headline",
              "slug",
              "lead_paragraph",
              "body",
              )
    prepopulated_fields = {"slug": ("headline",)}

    def get_queryset(self, request):
        this_type = ContentType.objects.get_for_model(News)
        qs = super().get_queryset(request)
        return qs.filter(content_type=this_type)

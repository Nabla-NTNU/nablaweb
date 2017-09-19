from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from content.admin import ContentAdmin
from .models import News
from .forms import NewsForm


@admin.register(News)
class NewsAdmin(ContentAdmin):
    form = NewsForm
    fields = ("publication_date",
              "published",
              "picture",
              "cropping",
              "headline",
              "slug",
              "lead_paragraph",
              "body",
              "priority",
              "allow_comments",
              )
    prepopulated_fields = {"slug": ("headline",)}

    def get_queryset(self, request):
        this_type = ContentType.objects.get_for_model(News)
        qs = super(NewsAdmin, self).get_queryset(request)
        return qs.filter(content_type=this_type)

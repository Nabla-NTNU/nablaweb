from news.models import News
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from news.forms import NewsForm
from content.admin import ContentAdmin


class NewsAdmin(ContentAdmin):
    form = NewsForm
    fields = ("picture",
              "cropping",
              "headline",
              "slug",
              "lead_paragraph",
              "body",
              "priority",
              "allow_comments")
    prepopulated_fields = {"slug": ("headline",)}

    def queryset(self, request):
        this_type = ContentType.objects.get_for_model(News)
        qs = super(NewsAdmin, self).queryset(request)
        return qs.filter(content_type=this_type)


admin.site.register(News, NewsAdmin)

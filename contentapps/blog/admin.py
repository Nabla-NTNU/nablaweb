from django.contrib import admin

from content.admin import ChangedByMixin
from .models import Blog, BlogPost


admin.site.register(Blog)


@admin.register(BlogPost)
class BlogPostAdmin(ChangedByMixin, admin.ModelAdmin):
    readonly_fields = ["view_counter"]
    ordering = ['-created_date']

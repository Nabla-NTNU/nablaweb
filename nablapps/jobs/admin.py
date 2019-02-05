"""
Admin interface for jobs app
"""
from nablapps.core.admin import ChangedByMixin
from django.contrib import admin
from image_cropping import ImageCroppingMixin
from nablapps.news.admin import add_to_frontpage
from .forms import AdvertForm, CompanyForm
from .models import Advert, Company, RelevantForChoices, TagChoices, YearChoices


admin.site.register(TagChoices)


@admin.register(Advert)
class AdvertAdmin(ChangedByMixin, admin.ModelAdmin):
    """Admin interface for Advert model"""
    fields = (
        "company",
        "headline",
        "slug",
        "lead_paragraph",
        "body",
        "info_website",
        "deadline_date",
        "removal_date",
        "relevant_for_group",
        "relevant_for_year",
        "info_file",
        "tags"
    )
    prepopulated_fields = {"slug": ("headline",)}
    form = AdvertForm
    actions = [add_to_frontpage]


@admin.register(Company)
class CompanyAdmin(ImageCroppingMixin, admin.ModelAdmin):
    """Admin interface for Company model"""
    prepopulated_fields = {"slug": ("name",)}
    fields = (
        "name",
        "picture",
        "cropping",
        "slug",
        "website",
        "description",
    )
    form = CompanyForm


@admin.register(RelevantForChoices, YearChoices)
class StaticModelAdmin(admin.ModelAdmin):
    """Class for hiding static models from admin for non authorized staff"""
    def get_model_perms(self, request):
        if not request.user.has_perm("jobs.can_see_static_models"):
            return {}
        return super().get_model_perms(request)

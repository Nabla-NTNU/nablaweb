from content.admin import ChangedByMixin
from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .forms import AdvertForm, CompanyForm
from .models import Advert, Company, RelevantForChoices, TagChoices, YearChoices


class AdvertAdmin(ChangedByMixin, admin.ModelAdmin):
    fields = (
        "company",
        "headline",
        "slug",
        "lead_paragraph",
        "body",
        "priority",
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


class CompanyAdmin(ImageCroppingMixin, admin.ModelAdmin):
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


class StaticModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        if request.user.has_perm("jobs.can_see_static_models"):
            return super(StaticModelAdmin, self).get_model_perms(request)
        else:
            return {}


admin.site.register(Advert, AdvertAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(RelevantForChoices, StaticModelAdmin)
admin.site.register(TagChoices)
admin.site.register(YearChoices, StaticModelAdmin)

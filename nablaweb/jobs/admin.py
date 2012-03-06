# -*- coding: utf-8 -*-

# Admingrensesnitt for stillingsannonser-appen

from django.contrib import admin
from django.forms import ModelForm
from django.forms import MultipleChoiceField
from jobs.models import Advert, Company, RelevantForChoices, TagChoices, YearChoices

#class RelevantForAdminForm(ModelForm):
#    RELEVANT_FOR_CHOICES = ((u'B', u'Biofysikk'), (u'T', u'Teknisk fysikk'), (u'I', u'Industriell matematikk'))
#    relevant_for = MultipleChoiceField(choices=RELEVANT_FOR_CHOICES)
#    class Meta:
#        model = Advert

class AdvertAdmin(admin.ModelAdmin):
    # relevant_for_form = RelevantForAdminForm
    pass
    
class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    fields = ("picture",
          "cropping",
          "name",
          "slug",
          "website",
          "description",)
    pass
        
class RelevantForChoicesAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        if request.user.is_superuser:
            return super(RelevantForChoicesAdmin, self).get_model_perms(request)
        if request.user.has_perm("jobs.can_see_static_models"):
            return {}
        else:
            return super(RelevantForChoicesAdmin, self).get_model_perms(request)
    
class TagChoicesAdmin(admin.ModelAdmin):
    pass
    
class YearChoicesAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        if request.user.is_superuser:
            return super(YearChoicesAdmin, self).get_model_perms(request)
        if request.user.has_perm("jobs.can_see_static_models"):
            return {}
        else:
            return super(YearChoicesAdmin, self).get_model_perms(request)

admin.site.register(Advert, AdvertAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(RelevantForChoices, RelevantForChoicesAdmin)
admin.site.register(TagChoices, TagChoicesAdmin)
admin.site.register(YearChoices, YearChoicesAdmin)

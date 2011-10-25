# -*- coding: utf-8 -*-

# Admingrensesnitt for com-appen

from django.contrib import admin
from django.forms import ModelForm, MultipleChoiceField
from com.models import ComPage, ComMember

class ComPageAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Komitéside"
        verbose_name_plural = "Komitésider"
        
class ComMemberAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Komitémedlem"
        verbose_name_plural = "Komitémedlemmer"

admin.site.register(ComPage, ComPageAdmin)
admin.site.register(ComMember, ComMemberAdmin)

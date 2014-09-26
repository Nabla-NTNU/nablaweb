# -*- coding: utf-8 -*-

# Admingrensesnitt for com-appen

from django.contrib import admin
from django.forms import ModelForm, MultipleChoiceField
from com.models import ComPage, ComMembership


class ComPageAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Komiteside"
        verbose_name_plural = "Komitesider"
        fields = '__all__'


class ComMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "com", "joined_date")
    ordering = ['-com']
    list_filter = ["com"]
    class Meta:
        verbose_name = "Komitemedlem"
        verbose_name_plural = "Komitemedlemmer"

admin.site.register(ComPage, ComPageAdmin)
admin.site.register(ComMembership, ComMembershipAdmin)

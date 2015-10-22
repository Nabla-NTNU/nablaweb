# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import NablaUser, NablaGroup, FysmatClass, RegistrationRequest
from .forms import NablaUserChangeForm, NablaUserCreationForm

User = get_user_model()


class GroupAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=FilteredSelectMultiple('Users', False),
        required=False)

    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            initial = kwargs.get('initial', {})
            initial['users'] = instance.user_set.all()
            kwargs['initial'] = initial
        super(GroupAdminForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        group = super(forms.ModelForm, self).save(commit=commit)

        if commit:
            group.user_set = self.cleaned_data['users']
        else:
            old_save_m2m = self.save_m2m

            def new_save_m2m():
                old_save_m2m()
                group.user_set = self.cleaned_data['users']

            self.save_m2m = new_save_m2m
        return group


class NablaGroupAdminForm(GroupAdminForm):
    class Meta:
        model = NablaGroup
        fields = '__all__'


class ExtendedGroupAdmin(GroupAdmin):
    form = GroupAdminForm


def maillist(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    url = reverse('mail_list', kwargs={'group': selected[0]})
    return HttpResponseRedirect(url)


maillist.short_description = "Vis mailliste"


class ExtendedNablaGroupAdmin(GroupAdmin):
    form = NablaGroupAdminForm
    actions = [maillist]


try:
    admin.site.unregister(Group)
except:
    pass

admin.site.register(Group, ExtendedGroupAdmin)
admin.site.register(NablaGroup, ExtendedNablaGroupAdmin)
admin.site.register(FysmatClass)


class NablaUserAdmin(UserAdmin):
    form = NablaUserChangeForm
    add_form = NablaUserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personlig informasjon'), {'fields': ('first_name', 'last_name', 'email', 'ntnu_card_number')}),
        (('Rettigheter'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
        ('Adresse og telefon', {'fields': ('address', 'mail_number', 'telephone', 'cell_phone',)}),
        ('Diverse', {'fields': ('birthday', 'web_page', 'about', 'wants_email')}),
    )


admin.site.register(NablaUser, NablaUserAdmin)


def reg_approve(modeladmin, request, queryset):
    for req in queryset:
        req.approve_request()
        req.delete()


def reg_decline(modeladmin, request, queryset):
    for req in queryset:
        req.delete()


class RegistrationRequestAdmin(admin.ModelAdmin):
    actions = [reg_approve, reg_decline]
    list_display = ['username', 'first_name', 'last_name', 'created']
    ordering = ['-created']

    class Meta:
        model = RegistrationRequest
        fields = '__all__'


admin.site.register(RegistrationRequest, RegistrationRequestAdmin)

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.encoding import smart_text

from .models import NablaUser, NablaGroup, FysmatClass, RegistrationRequest
from .forms import NablaUserChangeForm, NablaUserCreationForm


User = get_user_model()
admin.site.register(FysmatClass)
admin.site.unregister(Group)


# A subclass of ModelMultipleChoiceField that changes the label from the username to the full name of the user.
# Taken from: https://stackoverflow.com/questions/3966483/django-show-get-full-name-instead-or-username-in-model-form
class UserFullnameMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return smart_text(obj.get_full_name() + " - " + obj.username)


class GroupAdminForm(forms.ModelForm):
    users = UserFullnameMultipleChoiceField(queryset=User.objects.filter( is_active=True ),
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
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        group = super().save(commit=commit)

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


def maillist(modeladmin, request, queryset):
    s = '/'.join(str(g.id) for g in queryset)
    url = reverse('mail_list', kwargs={'groups': s})
    return HttpResponseRedirect(url)


maillist.short_description = "Vis mailliste"


@admin.register(NablaGroup)
class ExtendedNablaGroupAdmin(GroupAdmin):
    form = NablaGroupAdminForm
    actions = [maillist]


@admin.register(NablaUser)
class NablaUserAdmin(UserAdmin):
    form = NablaUserChangeForm
    add_form = NablaUserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personlig informasjon'), {'fields': ('first_name', 'last_name',
                                                'email', 'ntnu_card_number')}),
        (('Rettigheter'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
        ('Adresse og telefon', {'fields': ('address', 'mail_number', 'telephone', 'cell_phone',)}),
        ('Diverse', {'fields': ('birthday', 'web_page', 'about', 'wants_email')}),
        ('Avatar', {'fields': ('avatar', ) }),
    )


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    actions = ["approve", "decline"]
    list_display = ['username', 'first_name', 'last_name', 'created']
    ordering = ['-created']

    class Meta:
        model = RegistrationRequest
        fields = '__all__'

    def approve(self, request, queryset):
        for req in queryset:
            req.approve_request()
            req.delete()

    def decline(self, request, queryset):
        for req in queryset:
            req.delete()

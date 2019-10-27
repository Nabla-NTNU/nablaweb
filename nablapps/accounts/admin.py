"""
Admin for accounts app
"""
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.encoding import smart_text
from django.utils.translation import gettext_lazy as _

from .models import NablaUser, NablaGroup, FysmatClass, RegistrationRequest
from .forms import NablaUserChangeForm, NablaUserCreationForm


User = get_user_model()
admin.site.register(FysmatClass)
admin.site.unregister(Group)


class UserFullnameMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    Show both username and full name of the user

    Taken from:
    https://stackoverflow.com/questions/3966483/django-show-get-full-name-instead-or-username-in-model-form
    """
    def label_from_instance(self, obj):
        return smart_text(f"{obj.get_full_name()} - {obj.username}")


class GroupAdminForm(forms.ModelForm):
    """
    Custom form for Groups in admin.

    Adds a widget to add multiple users to a single group.
    This simplifies group membership administration.

    See also:
    https://djangosnippets.org/snippets/2452/
    """
    users = UserFullnameMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=FilteredSelectMultiple('Users', False),
        required=False)

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            initial = kwargs.setdefault('initial', {})
            initial['users'] = instance.user_set.all()
        super().__init__(*args, **kwargs)

    def _save_m2m(self):
        super()._save_m2m()
        self.instance.user_set.set(self.cleaned_data['users'])


def maillist(modeladmin, request, queryset):
    """
    Admin action for showing a list of email addresses for all users in selected groups
    """
    s = '/'.join(str(g.id) for g in queryset)
    url = reverse('mail_list', kwargs={'groups': s})
    return HttpResponseRedirect(url)


maillist.short_description = "Vis epostliste"


@admin.register(NablaGroup)
class ExtendedNablaGroupAdmin(GroupAdmin):
    """Admin for NablaGroup"""
    form = GroupAdminForm
    actions = [maillist]


@admin.register(NablaUser)
class NablaUserAdmin(UserAdmin):
    """Admin for NablaUser"""
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
        ('Avatar', {'fields': ('avatar', )}),
    )


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    """
    Admin interface for RegistrationRequest

    Meant to be used only to approve or decline the requests.
    """
    actions = ["approve", "decline"]
    list_display = ['username', 'first_name', 'last_name', 'created']
    ordering = ['-created']

    def approve(self, request, queryset):
        """Approve selected requests"""
        for req in queryset:
            req.approve_request()
            req.delete()

    def decline(self, request, queryset):
        """Decline selected requests"""
        for req in queryset:
            req.delete()


# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
    )

    def get_form(self,request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        sites = form.base_fields["sites"]
        sites.widget.can_add_related = False
        sites.widget.can_delete_related = False
        sites.widget.can_change_related = False
        return form

# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

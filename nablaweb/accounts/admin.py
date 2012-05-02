from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from accounts.models import GroupProfile, UserProfile



class GroupAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_active=True),
                                           widget=FilteredSelectMultiple('Users', False),
                                           required=False)
    class Meta:
        model = Group
        
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            initial = kwargs.get('initial', {})
            initial['users'] = instance.user_set.all()
            kwargs['initial'] = initial
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
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


class GroupProfileInline(admin.StackedInline):
    model = GroupProfile

class ExtendedGroupAdmin(GroupAdmin):
    form = GroupAdminForm
    inlines = GroupAdmin.inlines + [GroupProfileInline]

try:
    admin.site.unregister(Group)
except:
    pass

admin.site.register(Group, ExtendedGroupAdmin)

class UserProfileInlineForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('signature', 'signature_html','show_signatures','time_zone','autosubscribe','language','post_count',)

class UserProfileInline(admin.StackedInline):
    form = UserProfileInlineForm
    model = UserProfile

class ExtendedUserAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [UserProfileInline]

try:
    admin.site.unregister(User)
except:
    pass

admin.site.register(User, ExtendedUserAdmin)

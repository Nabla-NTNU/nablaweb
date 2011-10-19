from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from accounts.models import GroupProfile, UserProfile

class GroupProfileInline(admin.StackedInline):
    model = GroupProfile

class ExtendedGroupAdmin(GroupAdmin):
    inlines = GroupAdmin.inlines + [GroupProfileInline]

admin.site.register(Group, ExtendedGroupAdmin)


class UserProfileInline(admin.StackedInline):
    model = UserProfile

class ExtendedUserAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [UserProfileInline]

admin.site.register(User, ExtendedUserAdmin)

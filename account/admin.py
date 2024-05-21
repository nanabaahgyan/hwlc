from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserProfile
from contribution.models import NextOfKin

# Register your models here.
# Define an inline admin descriptor for Profile model
# which acts a bit like singleton


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = "User Profile"


class NextOfKinInline(admin.StackedInline):
    model = NextOfKin
    extra = 0

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, NextOfKinInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

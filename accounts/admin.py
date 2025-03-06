from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import Group
from .forms import CustomUserCreationForm, CustomChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    form = CustomUserCreationForm
    add_form = CustomUserCreationForm

    list_display = ["username", "email", "is_active", "is_staff", "is_admin"]
    list_filter = ["is_admin", "is_staff"]

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal Information", {"fields": ["username"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)

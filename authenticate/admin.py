from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from authenticate.models import CustomUser, UserProfile
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserModelAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "id",
        "username",
        "uuid",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "id",
        "username",
        "uuid",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "password",
                    "created_at",
                    "updated_at",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email", "id")


admin.site.register(CustomUser, CustomUserModelAdmin)
admin.site.register(UserProfile)

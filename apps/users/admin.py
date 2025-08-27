from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    # Add 'role' and 'cohort' to list display
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "cohort",
        "is_staff",
    )

    # Add filtering by role
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "groups")

    # Add role and cohort to search fields
    search_fields = ("username", "first_name", "last_name", "email", "cohort")

    # Add custom fields to the user form
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Role information"), {"fields": ("role", "cohort")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Add custom fields to add user form
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "role",
                    "cohort",
                ),
            },
        ),
    )


# Register the model with our custom admin class
admin.site.register(User, UserAdmin)

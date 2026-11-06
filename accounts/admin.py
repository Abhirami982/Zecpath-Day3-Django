
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "phone",
        "role",
        "is_active",
        "is_verified",
    )

    list_filter = (
        "role",
        "is_active",
        "is_verified",
    )

    search_fields = (
        "username",
        "email",
        "phone",
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": (
                "phone",
                "role",
                "is_verified",
            ),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {
            "fields": (
                "email",
                "phone",
                "role",
                "is_verified",
            ),
        }),
    )

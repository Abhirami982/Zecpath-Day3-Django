from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "candidate",
        "job",
        "status",
        "applied_at",
    )

    list_filter = ("status", "applied_at")

    search_fields = (
        "candidate__user__email",
        "job__title",
    )

    readonly_fields = ("applied_at", "updated_at")

    ordering = ("-applied_at",)
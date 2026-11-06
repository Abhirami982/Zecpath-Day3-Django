
from django.contrib import admin
from .models import Job, User, Application, Candidate, Employer


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "posted_at")
    search_fields = ("title", "company")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "role")
    list_filter = ("role",)
    search_fields = ("name", "email")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "applied_at")
    search_fields = ("user__name", "job__title")


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "skills")
    search_fields = ("full_name", "user__email")


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ("company_name", "user")
    search_fields = ("company_name", "user__email")

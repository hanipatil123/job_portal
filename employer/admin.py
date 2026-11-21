
from django.contrib import admin

from .models import EmployerProfile, Job, Application


# ==========================================
# EMPLOYER ADMIN
# ==========================================

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "company_email",
        "company_phone",
        "is_approved",
    )

    list_filter = ("is_approved",)

    search_fields = (
        "company_name",
        "company_email",
    )

    list_editable = ("is_approved",)


# ==========================================
# JOB ADMIN
# ==========================================

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "company_name",
        "location",
        "job_type",
        "salary",
        "vacancies",
        "application_deadline",
        "created_at",
    )

    search_fields = (
        "title",
        "company_name",
        "location",
    )

    list_filter = (
        "job_type",
        "application_deadline",
        "created_at",
    )

    readonly_fields = ("created_at",)


# ==========================================
# APPLICATION ADMIN
# ==========================================

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "applicant",
        "job",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
        "applied_at",
    )

    search_fields = (
        "applicant__username",
        "job__title",
    )


from django.contrib import admin
from .models import JobCategory, Employer, JobPosting


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'company_name',
        'email',
        'status',
        'created_at'
    )
    list_filter = ('status',)
    search_fields = ('company_name', 'email')


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'employer',
        'category',
        'location',
        'status'
    )
    list_filter = ('status', 'category')
    search_fields = ('title', 'location')

from django.contrib import admin
from .models import Job,JobApplication,JobSeekerProfile
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
 list_display=('title','company','location','job_type','active','created_at');list_filter=('job_type','active');search_fields=('title','company','location')
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
 list_display=('seeker','job','status','applied_at');list_filter=('status',);list_editable=('status',);search_fields=('seeker__username','job__title')
@admin.register(JobSeekerProfile)
class ProfileAdmin(admin.ModelAdmin):
 list_display=('user','phone','location','resume');search_fields=('user__username','location')

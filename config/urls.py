
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin Panel
    path("admin/", admin.site.urls),

    # Job Seeker Module - Member 1
    path("", include("job_seeker.urls")),

    # Employer Module - Member 2
    path("employer/", include("employer.urls")),
]

# Serve uploaded resumes and media during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

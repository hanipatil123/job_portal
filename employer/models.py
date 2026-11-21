
from django.conf import settings
from django.db import models


# ==========================================
# EMPLOYER PROFILE MODEL
# ==========================================

class EmployerProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employer_profile"
    )

    company_name = models.CharField(max_length=150)

    company_email = models.EmailField()

    company_phone = models.CharField(max_length=15)

    company_address = models.TextField(blank=True)

    company_description = models.TextField(blank=True)

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name


# ==========================================
# JOB MODEL
# ==========================================

class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
        ("Internship", "Internship"),
        ("Contract", "Contract"),
        ("Remote", "Remote"),
    ]

    employer = models.ForeignKey(
        EmployerProfile,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    title = models.CharField(max_length=200)

    company_name = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    description = models.TextField()

    location = models.CharField(max_length=150)

    job_type = models.CharField(
        max_length=30,
        choices=JOB_TYPE_CHOICES,
        default="Full Time"
    )

    salary = models.CharField(
        max_length=100,
        blank=True
    )

    experience = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    vacancies = models.PositiveIntegerField(default=1)

    qualification = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    skills_required = models.TextField(
        blank=True,
        default=""
    )

    application_deadline = models.DateField(
        null=True,
        blank=True
    )

    requirements = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ==========================================
# JOB APPLICATION MODEL
# ==========================================

class Application(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    resume = models.FileField(
        upload_to="resumes/",
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["job", "applicant"],
                name="unique_job_applicant"
            )
        ]

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST

from .models import EmployerProfile, Job, Application
from .forms import (
    EmployerRegistrationForm,
    EmployerProfileForm,
    JobForm,
)


# ==========================================
# EMPLOYER REGISTRATION
# ==========================================

def register(request):

    if request.method == "POST":
        form = EmployerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                "Registration successful! Please login."
            )
            return redirect("employer:login")

    else:
        form = EmployerRegistrationForm()

    return render(
        request,
        "employer/auth.html",
        {
            "form": form,
            "title": "Employer Registration",
            "button_text": "Register",
        }
    )


# ==========================================
# EMPLOYER LOGIN
# ==========================================

def employer_login(request):

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()

            if not EmployerProfile.objects.filter(
                user=user
            ).exists():
                form.add_error(
                    None,
                    "This account is not registered as an employer."
                )
            else:
                login(request, user)

                messages.success(
                    request,
                    "Login successful!"
                )

                return redirect("employer:dashboard")

    else:
        form = AuthenticationForm(request)

    return render(
        request,
        "employer/auth.html",
        {
            "form": form,
            "title": "Employer Login",
            "button_text": "Login",
        }
    )


# ==========================================
# EMPLOYER LOGOUT
# ==========================================

@require_POST
def employer_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("employer:login")


# ==========================================
# EMPLOYER DASHBOARD
# ==========================================

@login_required
def dashboard(request):

    profile = get_object_or_404(
        EmployerProfile,
        user=request.user
    )

    jobs = Job.objects.filter(
        employer=profile
    ).annotate(
        applicant_count=Count("applications")
    ).order_by("-created_at")

    applications = Application.objects.filter(
        job__employer=profile
    )

    context = {
        "profile": profile,
        "jobs": jobs,
        "total_jobs": jobs.count(),
        "total_applications": applications.count(),
        "shortlisted": applications.filter(
            status="shortlisted"
        ).count(),
        "rejected": applications.filter(
            status="rejected"
        ).count(),
        "pending": applications.filter(
            status="pending"
        ).count(),
    }

    return render(
        request,
        "employer/dashboard.html",
        context
    )


# ==========================================
# COMPANY PROFILE
# ==========================================

@login_required
def employer_profile(request):

    profile = get_object_or_404(
        EmployerProfile,
        user=request.user
    )

    if request.method == "POST":
        form = EmployerProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Company profile updated successfully!"
            )

            return redirect("employer:dashboard")

    else:
        form = EmployerProfileForm(
            instance=profile
        )

    return render(
        request,
        "employer/form.html",
        {
            "form": form,
            "title": "Edit Company Profile",
            "button_text": "Save Profile",
        }
    )


# ==========================================
# POST NEW JOB
# ==========================================

@login_required
def add_job(request):

    profile = get_object_or_404(
        EmployerProfile,
        user=request.user
    )

    if not profile.is_approved:
        messages.error(
            request,
            "Your employer account is not approved yet."
        )
        return redirect("employer:dashboard")

    if request.method == "POST":
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.employer = profile
            job.save()

            messages.success(
                request,
                "Job posted successfully!"
            )

            return redirect("employer:dashboard")

    else:
        form = JobForm(
            initial={
                "company_name": profile.company_name
            }
        )

    return render(
        request,
        "employer/form.html",
        {
            "form": form,
            "title": "Post New Job",
            "button_text": "Post Job",
        }
    )


# ==========================================
# EDIT JOB
# ==========================================

@login_required
def edit_job(request, job_id):

    profile = get_object_or_404(
        EmployerProfile,
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=profile
    )

    if not profile.is_approved:
        messages.error(
            request,
            "Your employer account is not approved yet."
        )
        return redirect("employer:dashboard")

    if request.method == "POST":
        form = JobForm(
            request.POST,
            instance=job
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Job updated successfully!"
            )

            return redirect("employer:dashboard")

    else:
        form = JobForm(instance=job)

    return render(
        request,
        "employer/form.html",
        {
            "form": form,
            "title": "Edit Job",
            "button_text": "Update Job",
        }
    )


# ==========================================
# DELETE JOB
# ==========================================

@login_required
@require_POST
def delete_job(request, job_id):

    profile = get_object_or_404(
        EmployerProfile,
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=profile
    )

    job.delete()

    messages.success(
        request,
        "Job deleted successfully!"
    )

    return redirect("employer:dashboard")


# ==========================================
# VIEW JOB APPLICANTS
# ==========================================

@login_required
def applicants(request, job_id):

    profile = get_object_or_404(
        EmployerProfile,
        user=request.user
    )

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=profile
    )

    applications = Application.objects.filter(
        job=job
    ).select_related(
        "applicant"
    ).order_by("-applied_at")

    return render(
        request,
        "employer/applicants.html",
        {
            "job": job,
            "applications": applications,
            "applicants": applications,
            "title": "Job Applicants",
        }
    )


# ==========================================
# SHORTLIST / REJECT APPLICANT
# ==========================================

@login_required
@require_POST
def update_status(request, application_id):

    profile = get_object_or_404(
        EmployerProfile,
        user=request.user
    )

    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=profile
    )

    status = request.POST.get("status", "").lower()

    if status not in ["pending", "shortlisted", "rejected"]:
        messages.error(
            request,
            "Invalid application status."
        )

    else:
        application.status = status
        application.save(update_fields=["status"])

        messages.success(
            request,
            "Applicant status updated successfully!"
        )

    return redirect(
        "employer:applicants",
        job_id=application.job.id
    )

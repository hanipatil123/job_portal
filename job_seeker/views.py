
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST

from .models import Job, JobApplication, JobSeekerProfile
from .forms import RegisterForm, LoginForm, ProfileForm, ApplyForm


# Home Page
def home(request):
    jobs = Job.objects.filter(active=True).order_by("-created_at")

    return render(request, "job_seeker/home.html", {
        "jobs": jobs[:6],
        "job_count": jobs.count(),
        "company_count": jobs.values("company").distinct().count(),
        "successful_applications": JobApplication.objects.filter(
            status="Selected"
        ).count(),
        "job_types": Job.TYPE_CHOICES,
    })


# Job Seeker Registration
def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        JobSeekerProfile.objects.get_or_create(user=user)
        login(request, user)

        messages.success(
            request,
            "Welcome! Complete your profile to stand out."
        )
        return redirect("profile")

    return render(request, "job_seeker/auth.html", {
        "form": form,
        "mode": "register",
    })


# Job Seeker Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("dashboard")

    return render(request, "job_seeker/auth.html", {
        "form": form,
        "mode": "login",
    })


# Logout
@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")


# Search and Filter Jobs
def jobs(request):
    qs = Job.objects.filter(active=True).order_by("-created_at")

    q = request.GET.get("q", "").strip()
    loc = request.GET.get("location", "").strip()
    kind = request.GET.get("type", "").strip()

    if q:
        qs = qs.filter(
            Q(title__icontains=q)
            | Q(company__icontains=q)
            | Q(description__icontains=q)
            | Q(requirements__icontains=q)
        )

    if loc:
        qs = qs.filter(location__icontains=loc)

    if kind:
        qs = qs.filter(job_type=kind)

    return render(request, "job_seeker/jobs.html", {
        "jobs": qs,
        "q": q,
        "location": loc,
        "selected_type": kind,
        "types": Job.TYPE_CHOICES,
    })


# Job Details
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, active=True)

    applied = (
        request.user.is_authenticated
        and JobApplication.objects.filter(
            seeker=request.user,
            job=job
        ).exists()
    )

    return render(request, "job_seeker/detail.html", {
        "job": job,
        "applied": applied,
    })


# Job Seeker Dashboard
@login_required
def dashboard(request):
    apps = JobApplication.objects.filter(
        seeker=request.user
    ).select_related("job")

    return render(request, "job_seeker/dashboard.html", {
        "apps": apps[:5],
        "total": apps.count(),
        "interviews": apps.filter(status="Interview").count(),
        "shortlisted": apps.filter(status="Shortlisted").count(),
        "recommendations": Job.objects.filter(
            active=True
        ).order_by("-created_at")[:3],
    })


# Profile and Resume Upload
@login_required
def profile(request):
    obj, _ = JobSeekerProfile.objects.get_or_create(
        user=request.user
    )

    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=obj
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Profile updated successfully."
        )
        return redirect("profile")

    return render(request, "job_seeker/profile.html", {
        "form": form,
        "profile": obj,
    })


# Apply for Job
@login_required
def apply(request, pk):
    job = get_object_or_404(Job, pk=pk, active=True)

    if JobApplication.objects.filter(
        seeker=request.user,
        job=job
    ).exists():
        messages.info(
            request,
            "You already applied for this job."
        )
        return redirect("applications")

    profile, _ = JobSeekerProfile.objects.get_or_create(
        user=request.user
    )

    if not profile.resume:
        messages.warning(
            request,
            "Upload your resume before applying."
        )
        return redirect("profile")

    form = ApplyForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        app = form.save(commit=False)
        app.job = job
        app.seeker = request.user
        app.save()

        messages.success(
            request,
            "Application submitted successfully!"
        )
        return redirect("applications")

    return render(request, "job_seeker/apply.html", {
        "job": job,
        "form": form,
        "profile": profile,
    })


# Track Job Applications
@login_required
def applications(request):
    apps = JobApplication.objects.filter(
        seeker=request.user
    ).select_related("job")

    return render(request, "job_seeker/applications.html", {
        "apps": apps,
    })

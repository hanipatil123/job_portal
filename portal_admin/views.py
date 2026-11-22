
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model
)
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST

from .models import JobCategory, Employer, JobPosting
from .forms import JobCategoryForm, JobPostingForm











# ==========================================
# ADMIN ACCESS DECORATOR
# ==========================================

def admin_required(view_func):
    return user_passes_test(
        lambda user: (
            user.is_authenticated
            and user.is_active
            and user.is_staff
        ),
        login_url='portal_admin:login'
    )(view_func)


# ==========================================
# 1. ADMIN LOGIN
# ==========================================

def admin_login(request):

    if (
        request.user.is_authenticated
        and request.user.is_active
        and request.user.is_staff
    ):
        return redirect('portal_admin:dashboard')

    error = None

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if (
            user is not None
            and user.is_active
            and user.is_staff
        ):
            login(request, user)
            return redirect('portal_admin:dashboard')

        error = "Invalid credentials or admin access denied."

    return render(
        request,
        'portal_admin/login.html',
        {'error': error}
    )


# ==========================================
# 2. ADMIN LOGOUT
# ==========================================

@require_POST
def admin_logout(request):
    logout(request)
    return redirect('portal_admin:login')


# ==========================================
# 3. ADMIN DASHBOARD
# ==========================================

@admin_required
def dashboard(request):

    User = get_user_model()

    context = {
        'total_users': User.objects.count(),
        'total_categories': JobCategory.objects.count(),
        'total_employers': Employer.objects.count(),
        'total_jobs': JobPosting.objects.count(),

        'active_jobs': JobPosting.objects.filter(
            status='active'
        ).count(),

        'pending_employers': Employer.objects.filter(
            status='pending'
        ).count(),

        'approved_employers': Employer.objects.filter(
            status='approved'
        ).count(),

        'rejected_employers': Employer.objects.filter(
            status='rejected'
        ).count(),
    }

    return render(
        request,
        'portal_admin/dashboard.html',
        context
    )


# ==========================================
# 4. VIEW ALL USERS
# ==========================================

@admin_required
def user_list(request):

    User = get_user_model()

    users = User.objects.all().order_by('-date_joined')

    return render(
        request,
        'portal_admin/users.html',
        {'users': users}
    )





# ==========================================
# 5. VIEW JOB CATEGORIES
# ==========================================

@admin_required
def category_list(request):

    categories = JobCategory.objects.all().order_by('name')

    return render(
        request,
        'portal_admin/categories.html',
        {'categories': categories}
    )


# ==========================================
# 6. ADD JOB CATEGORY
# ==========================================

@admin_required
def category_add(request):

    form = JobCategoryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('portal_admin:categories')

    return render(
        request,
        'portal_admin/category_form.html',
        {
            'form': form,
            'title': 'Add Job Category'
        }
    )


# ==========================================
# 7. EDIT JOB CATEGORY
# ==========================================

@admin_required
def category_edit(request, pk):

    category = get_object_or_404(JobCategory, pk=pk)

    form = JobCategoryForm(
        request.POST or None,
        instance=category
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('portal_admin:categories')

    return render(
        request,
        'portal_admin/category_form.html',
        {
            'form': form,
            'title': 'Edit Job Category'
        }
    )


# ==========================================
# 8. DELETE JOB CATEGORY
# ==========================================

@admin_required
@require_POST
def category_delete(request, pk):

    category = get_object_or_404(JobCategory, pk=pk)
    category.delete()

    return redirect('portal_admin:categories')


# ==========================================
# 9. VIEW ALL EMPLOYERS
# ==========================================

@admin_required
def employer_list(request):

    employers = Employer.objects.all().order_by('-created_at')

    return render(
        request,
        'portal_admin/employers.html',
        {'employers': employers}
    )


# ==========================================
# 10. APPROVE EMPLOYER
# ==========================================

@admin_required
@require_POST
def approve_employer(request, pk):

    employer = get_object_or_404(Employer, pk=pk)

    employer.status = 'approved'
    employer.save(update_fields=['status'])

    return redirect('portal_admin:employers')


# ==========================================
# 11. REJECT EMPLOYER
# ==========================================

@admin_required
@require_POST
def reject_employer(request, pk):

    employer = get_object_or_404(Employer, pk=pk)

    employer.status = 'rejected'
    employer.save(update_fields=['status'])

    return redirect('portal_admin:employers')


# ==========================================
# 12. VIEW ALL JOB POSTINGS
# ==========================================

@admin_required
def job_list(request):

    jobs = JobPosting.objects.select_related(
        'employer',
        'category'
    ).order_by('-created_at')

    return render(
        request,
        'portal_admin/jobs.html',
        {'jobs': jobs}
    )


# ==========================================
# 13. ADD JOB
# ==========================================

@admin_required
def job_add(request):

    form = JobPostingForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('portal_admin:jobs')

    return render(
        request,
        'portal_admin/job_form.html',
        {
            'form': form,
            'title': 'Add New Job'
        }
    )


# ==========================================
# 14. EDIT JOB
# ==========================================

@admin_required
def job_edit(request, pk):

    job = get_object_or_404(JobPosting, pk=pk)

    form = JobPostingForm(
        request.POST or None,
        instance=job
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('portal_admin:jobs')

    return render(
        request,
        'portal_admin/job_form.html',
        {
            'form': form,
            'title': 'Edit Job'
        }
    )


# ==========================================
# 15. DELETE JOB
# ==========================================

@admin_required
@require_POST
def job_delete(request, pk):

    job = get_object_or_404(JobPosting, pk=pk)
    job.delete()

    return redirect('portal_admin:jobs')


# ==========================================
# 16. ADMIN REPORTS
# ==========================================

@admin_required
def reports(request):

    User = get_user_model()

    context = {
        'total_users': User.objects.count(),
        'total_employers': Employer.objects.count(),
        'total_categories': JobCategory.objects.count(),
        'total_jobs': JobPosting.objects.count(),

        'pending_employers': Employer.objects.filter(
            status='pending'
        ).count(),

        'approved_employers': Employer.objects.filter(
            status='approved'
        ).count(),

        'rejected_employers': Employer.objects.filter(
            status='rejected'
        ).count(),

        'active_jobs': JobPosting.objects.filter(
            status='active'
        ).count(),

        'closed_jobs': JobPosting.objects.filter(
            status='closed'
        ).count(),
    }

    return render(
        request,
        'portal_admin/reports.html',
        context
    )


from django.urls import path
from . import views

app_name = "employer"

urlpatterns = [
    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.employer_login,
        name="login"
    ),

    path(
        "logout/",
        views.employer_logout,
        name="logout"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "profile/",
        views.employer_profile,
        name="profile"
    ),

    path(
        "jobs/new/",
        views.add_job,
        name="add_job"
    ),

    path(
        "jobs/<int:job_id>/edit/",
        views.edit_job,
        name="edit_job"
    ),

    path(
        "jobs/<int:job_id>/delete/",
        views.delete_job,
        name="delete_job"
    ),

    path(
        "jobs/<int:job_id>/applicants/",
        views.applicants,
        name="applicants"
    ),

    path(
        "applications/<int:application_id>/status/",
        views.update_status,
        name="update_status"
    ),
]

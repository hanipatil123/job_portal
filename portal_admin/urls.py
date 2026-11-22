
from django.urls import path
from . import views

app_name = 'portal_admin'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Login / Logout
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),

    # Users
    path('users/', views.user_list, name='users'),

    # Categories
    path('categories/', views.category_list, name='categories'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:pk>/',
         views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/',
         views.category_delete, name='category_delete'),

    # Employers
    path('employers/', views.employer_list, name='employers'),
    path('employers/<int:pk>/approve/',
         views.approve_employer, name='approve_employer'),
    path('employers/<int:pk>/reject/',
         views.reject_employer, name='reject_employer'),

    # Jobs
    path('jobs/', views.job_list, name='jobs'),
    path('jobs/add/', views.job_add, name='job_add'),
    path('jobs/<int:pk>/edit/',
         views.job_edit, name='job_edit'),
    path('jobs/<int:pk>/delete/',
         views.job_delete, name='job_delete'),

    path('reports/', views.reports, name='reports'),
]

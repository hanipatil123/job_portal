from django.urls import path
from . import views
urlpatterns=[path('',views.home,name='home'),path('register/',views.register_view,name='register'),path('login/',views.login_view,name='login'),path('logout/',views.logout_view,name='logout'),path('dashboard/',views.dashboard,name='dashboard'),path('profile/',views.profile,name='profile'),path('jobs/',views.jobs,name='jobs'),path('jobs/<int:pk>/',views.job_detail,name='job_detail'),path('jobs/<int:pk>/apply/',views.apply,name='apply'),path('applications/',views.applications,name='applications')]

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='system/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='system/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('overview/', views.overview, name='overview'),
    path('overview/manage_groups/', views.manage_groups, name='manage_groups'),
    path('overview/create_new_course/', views.CourseCreateView.as_view(), name='create_new_course'),
    path('overview/teacher_courses/', views.teacher_courses, name='teacher_courses'),
]

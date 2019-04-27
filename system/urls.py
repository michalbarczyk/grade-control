from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('overview/', views.overview, name='overview'),
    path('overview/manage_groups/', views.manage_groups, name='manage_groups'),
    path('overview/manage_groups/change_student_status/', views.change_student_status, name='change_student_status'),
    path('overview/manage_groups/change_teacher_status/', views.change_teacher_status, name='change_teacher_status'),
    path('overview/create_new_course/', views.CourseCreateView.as_view(), name='create_new_course'),
    path('overview/teacher_courses/', views.TeacherCourseListView.as_view(), name='teacher_courses'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
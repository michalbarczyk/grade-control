from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('overview/', overview, name='overview'),
    path('overview/manage_groups/', manage_groups, name='manage-groups'),
    path('overview/manage_groups/change_student_status/', change_student_status, name='change-student-status'),
    path('overview/manage_groups/change_teacher_status/', change_teacher_status, name='change-teacher-status'),
    path('overview/create_new_course/', CourseCreateView.as_view(), name='course-form'),
    path('overview/course_list/<slug:position>/', CourseListView.as_view(), name='course-list'),
    path('overview/course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
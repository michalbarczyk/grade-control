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
    path('overview/create_new_course/', CourseCreateView.as_view(), name='course-create'),
    path('overview/update_course/<int:pk>/', CourseUpdateView.as_view(), name='course-update'),
    path('overview/delete_course/<int:pk>/', CourseDeleteView.as_view(), name='course-delete'),
    path('overview/course_list/', CourseListView.as_view(), name='course-list'),
    path('overview/course_leave/<int:pk>/', CourseListView.as_view(), name='course-leave'),
    path('overview/course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('overview/course/<int:pk>/create_new_event/', EventCreateView.as_view(), name='event-form'),
    path('overview/course/<int:pk>/event_list/', EventListView.as_view(), name='see-events'),
    path('overview/course/<int:course_pk>/event_list/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('overview/course/<int:course_pk>/event_list/<int:pk>/manage_grades/', manage_grades, name='manage-grades'),
    path('overview/course/<int:pk>/manage_students/', manage_students, name='manage-students'),
    path('overview/search/', search, name='search'),
    path('overview/search/update_requesting/<int:pk>/', update_requesting, name='update-requesting'),
    path('overview/search/submit_request/', submit_request, name='submit-request')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

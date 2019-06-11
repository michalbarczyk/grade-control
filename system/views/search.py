from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from system.models import Course
from system.views import append_sidebar


@login_required
def search(request):
    q = request.GET.get('q', '')
    courses = None
    own_courses = None
    user = request.user
    if q:
        courses = Course.objects.filter(title__icontains=q)
        own_courses = courses.filter(students__user__username=user)
    leave_button = {'text': 'Leave', 'style': 'btn btn-danger'}
    join_button = {'text': 'Enroll', 'style': 'btn btn-success'}

    context = {
        'title': 'Search',
        'courses': courses,
        'own_courses': own_courses,
        'leave_button': leave_button,
        'join_button': join_button
    }
    context.update(append_sidebar(user))
    return render(request, 'system/search.html', context)

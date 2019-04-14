from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from system.models import Grade, Student


@login_required
def overview(request):
    user = request.user
    student_exists = Student.objects.filter(user=user.id).exists()
    groups = []
    if student_exists:
        grades = Grade.objects.filter(owner_id=user.id)
        groups += 'Student'
    else:
        grades = None
    context = {
        'sidebar': True,
        'groups': groups,
        'grades': grades,
        #'grades': request.user.grade_set.all(),
        'title': 'overview'
    }
    return render(request, 'system/overview.html', context)

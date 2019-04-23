from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from system.models import Grade, Student, Teacher


@login_required
def overview(request):
    user = request.user
    student_exists = Student.objects.filter(user=user.id).exists()
    if student_exists:
        grades = Grade.objects.filter(owner_id=user.id)
    else:
        grades = None

    context = {
        'grades': grades,
        'title': 'Overview'
    }
    context.update(append_sidebar(user))
    return render(request, 'system/overview.html', context)


def append_sidebar(user):
    student_exists = Student.objects.filter(user=user.id).exists()
    teacher_exists = Teacher.objects.filter(user=user.id).exists()
    groups = []
    if student_exists:
        groups.append('Student')
    if teacher_exists:
        groups.append('Teacher')

    student_str = ''
    teacher_str = ''
    if len(groups) > 1:
        student_str = ' (I learn)'
        teacher_str = ' (I teach)'

    return {'student_str': student_str, 'teacher_str': teacher_str, 'groups': groups, 'sidebar': True}
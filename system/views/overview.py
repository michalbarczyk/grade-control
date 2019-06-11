from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from system.models import AcademicGrade, Student, Teacher, ScoreGrade


@login_required
def overview(request):
    user = request.user
    if student_exists(user):
        grades = None #AcademicGrade.objects.filter(owner_id=user.id)
    else:
        grades = None

    context = {
        'grades': grades,
        'title': 'Overview'
    }
    context.update(append_sidebar(user))
    return render(request, 'system/overview.html', context)


def append_sidebar(user):
    groups = []
    if student_exists(user):
        groups.append('Student')
    if teacher_exists(user):
        groups.append('Teacher')

    student_str = ''
    teacher_str = ''
    if len(groups) > 1:
        student_str = ' (I learn)'
        teacher_str = ' (I teach)'

    return {'student_str': student_str, 'teacher_str': teacher_str, 'groups': groups, 'sidebar': True}


def student_exists(user):
    return Student.objects.filter(user=user.id).exists()


def teacher_exists(user):
    return Teacher.objects.filter(user=user.id).exists()
